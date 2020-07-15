import datetime
from datetime import date
from datetime import datetime
from dateutil import relativedelta

import requests
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, views
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import *
from .models import *


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def restricted(request, *args, **kwargs):
    return Response(data="ffff")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        # This data variable will contain refresh and access tokens
        data = super().validate(attrs)
        # You can add more User model's attributes like username,email etc. in the data dictionary like this.
        data['data'] = {'CCCNo': self.user.CCCNo, 'msisdn': self.user.msisdn}
        return data


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileListCreateView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def depend(request):
    if request.method == 'POST':
        data_copy = request.data.copy()
        data_copy.update({"user": request.user.id})
        serializer = DependantSerializer(data=data_copy)
        serializer.user = request.user
        print(serializer.is_valid())
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        queryset = Dependants.objects.filter(user=request.user.id)
        serializer = DependantSerializer(queryset, many=True)
        today = date.today()
        for d in serializer.data:
            dob = d["dob"]
            date1 = datetime.strptime(str(dob), '%Y-%m-%d')
            date2 = datetime.strptime(str(today), '%Y-%m-%d')
            r = relativedelta.relativedelta(date2, date1)
            months_difference = r.months + (12 * r.years)
            d["dob"] = months_difference
        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        data_copy = request.data.copy()
        a = check_ccc(request.data['CCCNo'])
        if a == False:
            return Response({"success": False, "error": "Invalid CCC number"}, status=status.HTTP_400_BAD_REQUEST)
        data_copy.update({"first_name": check_ccc(request.data['CCCNo'])["f_name"]})
        data_copy.update({"last_name": check_ccc(request.data['CCCNo'])["l_name"]})
        data_copy.update({"initial_facility": check_ccc(request.data['CCCNo'])["mfl_code"]})
        data_copy.update({"current_facility": check_ccc(request.data['CCCNo'])["mfl_code"]})

        serializer = UserSerializer(data=data_copy)
        if not serializer.is_valid():
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        if serializer.initial_data['password'] != serializer.initial_data['re_password']:
            raise serializers.ValidationError("Passwords don't match")
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True,
                                 "data": {
                                     "user": "User Created"
                                 }},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({"success": False, "error": [serializer.errors, str(e)]}, status=status.HTTP_400_BAD_REQUEST)


def check_ccc(value):
    user = {
        "ccc_number": value
    }

    url = "http://ushaurinode.mhealthkenya.org/api/mlab/get/one/client"
    headers = {
        'content-type': "application/json",
        'Accept': 'application/json'
    }
    response = requests.post(url, data=user, json=headers)
    try:
        return response.json()["clients"][0]
    except IndexError:
        return False


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_auth_user(request):
    if request.method == 'GET':
        queryset = User.objects.filter(id=request.user.id)
        dep = Dependants.objects.filter(user=request.user)
        dep_serializer = DependantSerializer(dep, many=True)
        serializer = UserProfileSerializer(queryset, many=True)
        serializer.data[0].update({"dependants": dep_serializer.data})
        serializer.data[0].update({"initial_facility": Facilities.objects.get(mfl_code=serializer.data[0]['initial_facility']).name})
        serializer.data[0].update({"current_facility": Facilities.objects.get(mfl_code=serializer.data[0]['current_facility']).name})

        return Response(data={"data": serializer.data}, status=status.HTTP_200_OK)


@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_user(request):
    if request.method == 'PUT':
        u = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(u, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_dependant(request):
    if request.method == 'PUT':
        u = Dependants.objects.get(id=request.data['id'])
        serializer = DependantUpdateSerializer(u, data=request.data)
        if u.user != request.user:
            raise serializers.ValidationError("Dependant is not registered to user")
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dependant(request, dep_id):
    if request.method == "GET":
        queryset = Dependants.objects.get(id=dep_id)
        if queryset.user != request.user:
            raise serializers.ValidationError("Dependant is not registered to user")
        today = date.today()
        serializer = DependantSerializer(queryset)
        dob = serializer.data["dob"]
        date1 = datetime.strptime(str(dob), '%Y-%m-%d')
        date2 = datetime.strptime(str(today), '%Y-%m-%d')
        r = relativedelta.relativedelta(date2, date1)
        months_difference = r.months + (12 * r.years)
        serializer.data["dob"] = months_difference
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# class UserLogoutAllView(views.APIView):
#     """
#     Use this endpoint to log out all sessions for a given user.
#     """
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request, *args, **kwargs):
#         user = request.user
#         user.jwt_secret = uuid.uuid4()
#         user.save()
#         return Response(status=status.HTTP_200_OK)
