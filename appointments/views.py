import datetime
from datetime import date
from datetime import datetime
from dateutil import relativedelta

import requests
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import *
from .serializer import *


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_appointment(request):
    if request.method == 'GET':
        c = check_appoint(request.user.CCCNo)
        if not c["success"]:
            return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        li = []
        ar = Appointments.objects.filter(user=request.user).count()
        if ar != len(c["appointments"]):
            for it in range(len(c["appointments"])):
                r = Appointments.objects.filter(user=request.user)
                # for a in r:
                #     print(r)
                #     if a.appntmnt_date == c["appointments"][it]["appntmnt_date"] and a.app_status == c["appointments"][it]["app_status"] and a.visit_type == c["appointments"][it]["visit_type"]:
                #         break
                #     else:
                #         data = Appointments()
                #         data.user = request.user
                #         data.appntmnt_date = c["appointments"][it]["appntmnt_date"]
                #         data.app_status = c["appointments"][it]["app_status"]
                #         data.visit_type = c["appointments"][it]["visit_type"]
                #         data.save()
        r = Appointments.objects.filter(user=request.user)
        serializer = AppointSerializer(c["appointments"], many=True)
        # li.append(serializer.data[0])
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def upcoming_appointment(request):
    if request.method == 'GET':
        c = check_appoint(request.user.CCCNo)
        if not c["success"]:
            return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        li = []
        for it in range(len(c["appointments"])):
            if datetime.strptime(str(date.today()), '%Y-%m-%d') < datetime.strptime(str(c["appointments"][it]["appntmnt_date"]), '%Y-%m-%d'):
                li.append(c["appointments"][it])
        serializer = AppointSerializer(li, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def past_appointment(request):
    if request.method == 'GET':
        c = check_appoint(request.user.CCCNo)
        if not c["success"]:
            return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        li = []
        for it in range(len(c["appointments"])):
            if datetime.strptime(str(date.today()), '%Y-%m-%d') > datetime.strptime(str(c["appointments"][it]["appntmnt_date"]), '%Y-%m-%d'):
                li.append(c["appointments"][it])
        serializer = AppointSerializer(li, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


def check_appoint(value):
    try:
        user = {
            "ccc_number": value
        }

        url = "http://ushaurinode.mhealthkenya.org/api/mlab/get/appointments"
        headers = {
            'content-type': "application/json",
            'Accept': 'application/json'
        }
        response = requests.post(url, data=user, json=headers)
        return response.json()
    except ConnectionError as e:
        print(e)
