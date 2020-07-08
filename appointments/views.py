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
        for it in range(len(c["client"]["appointments"])):
            r = Appointments.objects.filter(aid=c["client"]["appointments"][it]["id"]).count()
            if r == 0:
                data = Appointments()
                data.user = request.user
                data.aid = c["client"]["appointments"][it]["id"]
                data.appntmnt_date = c["client"]["appointments"][it]["appntmnt_date"]
                data.app_status = c["client"]["appointments"][it]["app_status"]
                data.visit_type = c["client"]["appointments"][it]["visit_type"]
                data.appoint_type = c["client"]["appointments"][it]["app_type"]["name"]
                data.save()
        r = Appointments.objects.filter(user=request.user)
        print(r)
        serializer = AppointSerializer(r, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def upcoming_appointment(request):
    if request.method == 'GET':
        c = check_appoint(request.user.CCCNo)
        if not c["success"]:
            return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        li = []
        for it in range(len(c["client"]["appointments"])):
            if datetime.strptime(str(date.today()), '%Y-%m-%d') <= datetime.strptime(str(c["client"]["appointments"][it]["appntmnt_date"]), '%Y-%m-%d'):
                c["client"]["appointments"][it].update({"app_type": c["client"]["appointments"][it]["app_type"]["name"]})
                li.append(c["client"]["appointments"][it])
                r = Appointments.objects.filter(aid=c["client"]["appointments"][it]["id"]).count()
                if r == 0:
                    data = Appointments()
                    data.user = request.user
                    data.aid = c["client"]["appointments"][it]["id"]
                    data.appntmnt_date = c["client"]["appointments"][it]["appntmnt_date"]
                    data.app_status = c["client"]["appointments"][it]["app_status"]
                    data.visit_type = c["client"]["appointments"][it]["visit_type"]
                    data.appoint_type = c["client"]["appointments"][it]["app_type"]["name"]
                    data.save()
            if len(li) == 0:
                return Response(data={'message': "No upcoming appointmets"}, status=status.HTTP_204_NO_CONTENT)
        serializer = PAppointSerializer(li, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def past_appointment(request):
    if request.method == 'GET':
        c = check_appoint(request.user.CCCNo)
        if not c["success"]:
            return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        li = []
        for it in range(len(c["client"]["appointments"])):
            if datetime.strptime(str(date.today()), '%Y-%m-%d') > datetime.strptime(str(c["client"]["appointments"][it]["appntmnt_date"]), '%Y-%m-%d'):
                c["client"]["appointments"][it].update({"app_type": c["client"]["appointments"][it]["app_type"]["name"]})
                li.append(c["client"]["appointments"][it])
                r = Appointments.objects.filter(aid=c["client"]["appointments"][it]["id"]).count()
                if r == 0:
                    data = Appointments()
                    data.user = request.user
                    data.aid = c["client"]["appointments"][it]["id"]
                    data.appntmnt_date = c["client"]["appointments"][it]["appntmnt_date"]
                    data.app_status = c["client"]["appointments"][it]["app_status"]
                    data.visit_type = c["client"]["appointments"][it]["visit_type"]
                    data.appoint_type = c["client"]["appointments"][it]["app_type"]["name"]
                    data.save()
        if len(li) == 0:
            return Response(data={'message': "No upcoming appointmets"}, status=status.HTTP_204_NO_CONTENT)
        serializer = PAppointSerializer(li, many=True)
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
