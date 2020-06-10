import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from authApp.models import *
from .serializer import *


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_vload(request):
    if request.method == 'GET':
        c = check_lab(request.user.CCCNo)
        if c == {'message': 'No results for the given CCC Number were found'}:
            return Response(data={'message': 'No results for the given CCC Number were found'}, status=status.HTTP_204_NO_CONTENT)
        r = VLResult.objects.filter(r_id=c["results"][0]["id"])
        if r.count() == 0:
            data = VLResult()
            data.user = request.user
            data.r_id = c["results"][0]["id"]
            data.result_type = c["results"][0]["result_type"]
            try:
                data.result_content = int(c["results"][0]["result_content"])
            except ValueError:
                data.result_content = c["results"][0]["result_content"][:-9]
            data.date_collected = c["results"][0]["date_collected"]
            data.lab_name = c["results"][0]["lab_name"]
            data.save()
        r = VLResult.objects.filter(r_id=c["results"][0]["id"], result_type="1")
        serializer = VLSerializer(r, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_eid(request):
    if request.method == 'GET':
        ret = []
        d = Dependants.objects.filter(user=request.user)
        for a in d:
            print(a.heiNumber)
            c = check_lab(a.heiNumber)
            print(c)
            if c == {'message': 'No results for the given CCC Number were found'}:
                c.update({"hei": a.heiNumber})
                ret.append(c)
                continue
            r = EidResults.objects.filter(r_id=c["results"][0]["id"])
            if r.count() == 0:
                data = EidResults()
                data.dependant = a
                data.r_id = c["results"][0]["id"]
                data.result_type = c["results"][0]["result_type"]
                data.result_content = c["results"][0]["result_content"]
                data.date_collected = c["results"][0]["date_collected"]
                data.lab_name = c["results"][0]["lab_name"]
                data.save()
            r = EidResults.objects.filter(r_id=c["results"][0]["id"], result_type="2")
            serializer = EidSerializer(r, many=True)
            print(len(serializer.data))
            for i in range(len(serializer.data)):
                serializer.data[i].update({"dependant": a.heiNumber})
            ret.append(serializer.data)
        return Response(data={"data": ret}, status=status.HTTP_200_OK)


def check_lab(value):
    try:
        user = {
            "ccc_number": value
        }

        url = "https://mlab.mhealthkenya.co.ke/api/ushauri/get/results"
        headers = {
            'content-type': "application/json",
            'Accept': 'application/json'
        }
        response = requests.post(url, data=user, json=headers, verify=False)
        return response.json()
    except ConnectionError as e:
        print(e)
