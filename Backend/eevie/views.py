from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets,status,permissions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404
from django.db import connection
from eevie.serializers import *
from eevie.models import *
import json,datetime
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
def SessionsPerPoint(request, pk, date_from, date_to):
    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00+00:00"
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00+00:00"

    station = Station.objects.all().filter(id=int(pk))

    if station == None:
        return Response({'status': 'Failed'})

    sessions = station.sessions.all()

    sesh = [] 
    index = 1
    for i in sessions:
        temp = {}
        temp['SessionIndex'] = index
        temp['SessionID'] = i.id
        temp['StartedOn'] = i.connectionTime
        temp['FinishedOn'] = i.disconnectTime
        temp['Protocol'] = i.point.protocol
        temp['EnergyDelivered'] = i.kWhDelivered
        temp['Payment'] = i.payment
        temp['VehicleType'] = i.vehicle.car.type
        index += 1
        sesh.append(temp)

    serializer = {}

    serializer['Point'] = station.id
    serializer['PointOperator'] = station.operators.title
    serializer['RequestTimesamp'] = datetime.datetime.now()
    serializer['PeriodFrom'] = date_from
    serializer['PeriodTo'] = date_to
    serializer['NumberOfChargingSessions'] = sessions.count()
    
    return Response(serializer)

class UserViewSet(APIView): 
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ObtainTokenPairWithUsernameView(TokenObtainPairView):     #refresh and access token
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

            
class CustomerViewSet(viewsets.ModelViewSet):
    
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()   
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class HealthCheckView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            one = cursor.fetchone()[0]
            if one != 1:
                raise Response({'status':'failed'})
        return Response({'status':'OK'})
