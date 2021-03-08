from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets,status,permissions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse, response
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_csv.renderers import JSONRenderer,CSVRenderer
from django.shortcuts import get_object_or_404
from django.db import connection
from eevie.serializers import *
from eevie.models import *
import json,datetime
from pytz import timezone
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
from django.db.models import Count, Sum
import pandas as pd
import csv


class CurrentUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@api_view(['GET'])
@renderer_classes([JSONRenderer,CSVRenderer])
def SessionsPerPoint(request, pk, date_from, date_to, format):
    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00" ##ισως χρειαστε να αλλαξω το date_from[4:6] με το μηδενικο
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        point = Point.objects.get(id=int(pk))
    except Point.DoesNotExist:
        return Response({'Point': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = point.points.all().filter(connectionTime__range=[date_from,date_to])

    point_info = {}

    point_info['Point'] = point.id
    first = point.station.operators.all().first()
    if first is not None:
        point_info['PointOperator'] = first.title
    else:
        point_info['PointOperator'] = "Unknown"
    point_info['RequestTimesamp'] = datetime.datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    point_info['PeriodFrom'] = date_from[:-9]
    point_info['PeriodTo'] = date_to[:-9]
    point_info['NumberOfChargingSessions'] = sessions.count()

    sessionslist = [] 
    index = 1
    for i in sessions:
        temp = {}
        temp['SessionIndex'] = index
        temp['SessionID'] = i.id
        temp['StartedOn'] = i.connectionTime.strftime("%Y-%m-%d %H:%M:%S")
        temp['FinishedOn'] = i.disconnectTime.strftime("%Y-%m-%d %H:%M:%S")
        temp['Protocol'] = i.point.protocol
        temp['EnergyDelivered'] = i.kWhDelivered
        temp['Payment'] = i.payment
        temp['VehicleType'] = i.vehicle.car.type
        index += 1
        sessionslist.append(temp.copy())

    point_info['ChargingSessionsList'] = sessionslist[:]

    # format = request.GET.get('format', None)
    # if format == 'csv':
    #     response = HttpResponse(content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="data.csv"'
    #     pdObj = pd.read_json(point_info)
    #     print(pdObj)

    return Response(point_info, status=status.HTTP_200_OK)

@api_view(['GET'])
def SessionsPerStation(request, pk, date_from, date_to):

    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00"
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        station = Station.objects.get(id=int(pk))
    except Station.DoesNotExist:
        return Response({'Station': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = station.sessions.all().filter(connectionTime__range=[date_from,date_to])

    station_info = {}
    station_info['StationID'] = station.id
    if station.operators.all().first() is not None:
        station_info['Operator'] = station.operators.all().first().title
    else:
        station_info['Operator'] = "Unknown"
    station_info['RequestTimestamp'] = datetime.datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    station_info['PeriodFrom'] = date_from[:-9]
    station_info['PeriodTo'] = date_to[:-9]
    station_info['TotalEnergyDelivered']=sessions.aggregate(Sum('kWhDelivered'))['kWhDelivered__sum']
    station_info['NumberOfChargingSessions'] = sessions.count()
    station_info['NumberOfActivePoints'] = len(sessions.values('point').annotate(Count('point__id')))
    station_info['SessionsSummaryList'] = list(sessions.values('point__id').annotate(PointSessions=Count('point'), EnergyDelivered = Sum('kWhDelivered')).order_by('-PointSessions'))

    return Response(station_info, status=status.HTTP_200_OK)

@api_view(['GET'])
def SessionsPerEV(request, pk, date_from, date_to):
    
    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00"
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        vehicle = Car.objects.get(id=int(pk))
    except Car.DoesNotExist:
        return Response({'Car': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = vehicle.vehicle.all().filter(connectionTime__range=[date_from,date_to])

    ev_info = {}
    ev_info['VehicleID'] = vehicle.id
    ev_info['RequestTimestamp'] = datetime.datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    ev_info['PeriodFrom'] = date_from[:-9]
    ev_info['PeriodTo'] = date_to[:-9]
    kWh = sessions.aggregate(Sum('kWhDelivered'))['kWhDelivered__sum'] #average consumption ??
    if kWh is not None:
        ev_info['TotalEnergyConsumed']=kWh
    else:
        ev_info['TotalEnergyConsumed']=0
    ev_info['NumberOfVisitedPoints'] = len(sessions.values('point').annotate(Count('point__id')))
    ev_info['NumberOfVehicleChargingSessions'] = sessions.count()

    sessionslist = [] 
    index = 1
    for i in sessions:
        temp = {}
        temp['SessionIndex'] = index
        temp['SessionID'] = i.id
        temp['EnergyProvider'] = i.provider.name
        temp['StartedOn'] = i.connectionTime.strftime("%Y-%m-%d %H:%M:%S")
        temp['FinishedOn'] = i.disconnectTime.strftime("%Y-%m-%d %H:%M:%S")
        temp['EnergyDelivered'] = i.kWhDelivered
        temp['PricePolicyRef'] = i.payment #have to change
        temp['CostPerKWh'] = i.provider.costPerkWh
        temp['SessionCost'] = i.kWhDelivered*i.provider.costPerkWh
        index += 1
        sessionslist.append(temp.copy())

    ev_info['VehicleChargingSessionsList'] = sessionslist[:]

    return Response(ev_info, status=status.HTTP_200_OK)

@api_view(['GET'])
def SessionsPerProvider(request, pk, date_from, date_to):
    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00"
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        provider = Provider.objects.get(id=int(pk))
    except Provider.DoesNotExist:
        return Response({'provider': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = provider.hasmade.all().filter(connectionTime__range=[date_from,date_to])

    provider_info = {}
    provider_info['ProviderID'] = provider.id
    provider_info['ProviderName'] = provider.name
    provider_info['CostPerKWh'] = provider.costPerkWh
    
    sessionslist = [] 
    for session in sessions:

        temp = {}
        temp['StationID'] = session.station.id
        temp['SessionID'] = session.id
        temp['VehicleID'] = session.vehicle.id
        temp['StartedOn'] = session.connectionTime.strftime("%Y-%m-%d %H:%M:%S")
        temp['FinishedOn'] = session.disconnectTime.strftime("%Y-%m-%d %H:%M:%S")
        temp['EnergyDelivered'] = session.kWhDelivered
        temp['PricePolicyRef'] = session.payment #have to change
        temp['TotalCost'] = session.kWhDelivered*provider.costPerkWh

        sessionslist.append(temp.copy())

    provider_info['ProviderChargingSessionsList'] = sessionslist[:]

    return Response(provider_info, status=status.HTTP_200_OK)


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


        