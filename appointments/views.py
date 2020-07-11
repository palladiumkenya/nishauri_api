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
            pull_dep(request)
            if Appointments.objects.filter(user=request.user).count() > 0:
                serializer = AppointSerializer(Appointments.objects.filter(user=request.user), many=True)
                return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        pull_dep(request)
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
        li = []
        if not c["success"]:
            pull_dep(request)
            if Appointments.objects.filter(user=request.user).count() > 0:
                for r in Appointments.objects.filter(user=request.user):
                    if datetime.strptime(str(date.today()), '%Y-%m-%d') <= datetime.strptime(str(r.appntmnt_date), '%Y-%m-%d'):
                        li.append(r)
                if len(li) == 0:
                    return Response(data={'message': "No upcoming appointmets"}, status=status.HTTP_204_NO_CONTENT)
                serializer = AppointSerializer(li, many=True)
                return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        pull_dep(request)
        for it in range(len(c["client"]["appointments"])):
            r = Appointments.objects.filter(aid=c["client"]["appointments"][it]["id"])
            if r.count() == 0:
                data = Appointments()
                data.user = request.user
                data.aid = c["client"]["appointments"][it]["id"]
                data.appntmnt_date = c["client"]["appointments"][it]["appntmnt_date"]
                data.app_status = c["client"]["appointments"][it]["app_status"]
                data.visit_type = c["client"]["appointments"][it]["visit_type"]
                data.appoint_type = c["client"]["appointments"][it]["app_type"]["name"]
                data.save()

        for r in Appointments.objects.filter(user=request.user):
            if datetime.strptime(str(date.today()), '%Y-%m-%d') <= datetime.strptime(str(r.appntmnt_date), '%Y-%m-%d'):
                li.append(r)

        if len(li) == 0:
            return Response(data={'message': "No upcoming appointmets"}, status=status.HTTP_204_NO_CONTENT)
        serializer = AppointSerializer(li, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def past_appointment(request):
    if request.method == 'GET':
        c = check_appoint(request.user.CCCNo)
        li = []
        if not c["success"]:
            pull_dep(request)
            if Appointments.objects.filter(user=request.user).count() > 0:
                for r in Appointments.objects.filter(user=request.user):
                    if datetime.strptime(str(date.today()), '%Y-%m-%d') > datetime.strptime(str(r.appntmnt_date), '%Y-%m-%d'):
                        li.append(r)
                if len(li) == 0:
                    return Response(data={'message': "No upcoming appointmets"}, status=status.HTTP_204_NO_CONTENT)
                serializer = AppointSerializer(li, many=True)
                return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        pull_dep(request)
        for it in range(len(c["client"]["appointments"])):
            r = Appointments.objects.filter(aid=c["client"]["appointments"][it]["id"])
            if r.count() == 0:
                data = Appointments()
                data.user = request.user
                data.aid = c["client"]["appointments"][it]["id"]
                data.appntmnt_date = c["client"]["appointments"][it]["appntmnt_date"]
                data.app_status = c["client"]["appointments"][it]["app_status"]
                data.visit_type = c["client"]["appointments"][it]["visit_type"]
                data.appoint_type = c["client"]["appointments"][it]["app_type"]["name"]
                data.save()

        for r in Appointments.objects.filter(user=request.user):
            if datetime.strptime(str(date.today()), '%Y-%m-%d') > datetime.strptime(str(r.appntmnt_date), '%Y-%m-%d'):
                li.append(r)
        if len(li) == 0:
            return Response(data={'message': "No upcoming appointmets"}, status=status.HTTP_204_NO_CONTENT)
        serializer = AppointSerializer(li, many=True)
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['POST', 'GET'])
def book_appointment(request):
    if request.method == 'POST':
        data_copy = request.data.copy()
        data_copy.update({"user": request.user.id})
        serializer = BookAppointmentSerializer(data=data_copy)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    else:
        appoi = BookAppointment.objects.filter(user=request.user)#, book_type="New")
        serializer = BookAppointmentSerializer(appoi, many=True)
        for k in serializer.data:
            if k["book_type"] == "Edit":
                k.update({"appointment":AppointSerializer(Appointments.objects.filter(id=k["book_id"]), many=True).data[0]})
        if len(serializer.data) > 0:
            return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': "No rescheduled appointments"}, status=status.HTTP_400_BAD_REQUEST)



@permission_classes([IsAuthenticated])
@api_view(['POST'])
def reschedule_appointment(request, app_id):
    if request.method == 'POST':
        data_copy = request.data.copy()
        data_copy.update({"user": request.user.id, "book_id": app_id, "book_type": "Edit"})
        serializer = BookAppointmentSerializer(data=data_copy)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_treatment(request):
    try:
        user = {
            "ccc_number": request.user.CCCNo
        }

        url = "http://ushaurinode.mhealthkenya.org/api/mlab/get/one/client"
        headers = {
            'content-type': "application/json",
            'Accept': 'application/json'
        }
        response = requests.post(url, data=user, json=headers)
        if len(response.json()["clients"]) > 0:
            return Response(data={"treatment": response.json()["clients"][0]["client_status"]}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': "No treatments found"}, status=status.HTTP_400_BAD_REQUEST)

    except ConnectionError as e:
        print(e)


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


def pull_dep(r):
    dep = Dependants.objects.filter(user=r.user)
    for d in dep:
        c = check_appoint(d.heiNumber)
        print(c)
        if not c["success"]:
            return Response(data={'message': c["message"]}, status=status.HTTP_204_NO_CONTENT)
        for it in range(len(c["client"]["appointments"])):
            r = Appointments.objects.filter(aid=c["client"]["appointments"][it]["id"]).count()
            if r == 0:
                data = Appointments()
                data.user = r.user
                data.aid = c["client"]["appointments"][it]["id"]
                data.appntmnt_date = c["client"]["appointments"][it]["appntmnt_date"]
                data.app_status = c["client"]["appointments"][it]["app_status"]
                data.visit_type = c["client"]["appointments"][it]["visit_type"]
                data.dependant = d.heiNumber
                data.owner = "Dependant"
                data.appoint_type = c["client"]["appointments"][it]["app_type"]["name"]
                data.save()
