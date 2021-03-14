from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.functional import empty
from django.http import HttpResponse, response
from rest_framework import viewsets,status,permissions
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.renderers import MultiPartRenderer
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes, renderer_classes
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_csv.renderers import JSONRenderer,CSVRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.db import connection
from eevie.serializers import *
from eevie.models import *
from eevie.fill_db import setUpSessions
import json
from datetime import datetime
from pytz import timezone
# Create your views here.
from django.db.models import Count, Sum
import codecs, csv

@api_view(['GET'])
@renderer_classes([JSONRenderer,CSVRenderer])
def SessionsPerPoint(request, pk, date_from, date_to):        
    
    if not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00" ##ισως χρειαστε να αλλαξω το date_from[4:6] με το μηδενικο
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        point = Point.objects.get(id=int(pk))
    except Point.DoesNotExist:
        return Response({'Point': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = point.points.all().filter(connectionTime__range=[date_from,date_to]).order_by('connectionTime')

    point_info = {}

    point_info['Point'] = point.id
    first = point.station.operators.all().first()
    if first is not None:
        point_info['PointOperator'] = first.title
    else:
        point_info['PointOperator'] = "Unknown"
    point_info['RequestTimesamp'] = datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
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

    return Response(point_info, status=status.HTTP_200_OK)

@api_view(['GET'])
@renderer_classes([JSONRenderer,CSVRenderer])
def SessionsPerStation(request, pk, date_from, date_to):

    if not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00"
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        station = Station.objects.get(id=int(pk))
    except Station.DoesNotExist:
        return Response({'Station': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = station.sessions.all().filter(connectionTime__range=[date_from,date_to]).order_by('connectionTime')

    station_info = {}
    station_info['StationID'] = station.id
    if station.operators.all().first() is not None:
        station_info['Operator'] = station.operators.all().first().title
    else:
        station_info['Operator'] = "Unknown"
    station_info['RequestTimestamp'] = datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
    station_info['PeriodFrom'] = date_from[:-9]
    station_info['PeriodTo'] = date_to[:-9]
    station_info['TotalEnergyDelivered']=sessions.aggregate(Sum('kWhDelivered'))['kWhDelivered__sum']
    station_info['NumberOfChargingSessions'] = sessions.count()
    station_info['NumberOfActivePoints'] = len(sessions.values('point').annotate(Count('point__id')))
    station_info['SessionsSummaryList'] = list(sessions.values('point__id').annotate(PointSessions=Count('point'), EnergyDelivered = Sum('kWhDelivered')).order_by('-PointSessions'))

    return Response(station_info, status=status.HTTP_200_OK)

@api_view(['GET'])
@renderer_classes([JSONRenderer,CSVRenderer])
def SessionsPerEV(request, pk, date_from, date_to):
    
    if not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00"
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        vehicle = Car.objects.get(id=int(pk))
    except Car.DoesNotExist:
        return Response({'Car': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = vehicle.vehicle.all().filter(connectionTime__range=[date_from,date_to]).order_by('connectionTime')

    ev_info = {}
    ev_info['VehicleID'] = vehicle.id
    ev_info['RequestTimestamp'] = datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
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
@renderer_classes([JSONRenderer,CSVRenderer])
def SessionsPerProvider(request, pk, date_from, date_to):
    
    if not request.user.is_superuser:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    date_from = date_from[0:4] + "-" + date_from[4:6] + "-" + date_from[6:8] + " 00:00:00.00+00:00"
    date_to = date_to[0:4] + "-" + date_to[4:6] + "-" + date_to[6:8] + " 00:00:00.00+00:00"

    try:
        provider = Provider.objects.get(id=int(pk))
    except Provider.DoesNotExist:
        return Response({'provider': ['Not Found']}, status=status.HTTP_400_BAD_REQUEST)

    sessions = provider.hasmade.all().filter(connectionTime__range=[date_from,date_to]).order_by('connectionTime')

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


class UserView(APIView): 
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self,request,format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            car = CarBase.objects.filter(id=request.data['car_id'])
            user = User.objects.filter(username=request.data['username'])
            if not user:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if car:
                Car.objects.create(car=car.first(), customer=user.first())
                
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteMe(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self,request):
        request.user.delete()
        return Response({'message':'User successfully deleted.'}, status=status.HTTP_200_OK)

class ObtainTokenPairWithUsernameView(TokenObtainPairView):     #refresh and access token
    permission_classes = (permissions.AllowAny,)
    authentication_classes = []
    serializer_class = MyTokenObtainPairSerializer

class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
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

class CurrentUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ResetSessions(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        Session.objects.all().delete()

        try:
            User.objects.get(username = 'admin')
        except User.DoesNotExist:
            User.objects.create(username = 'admin', password = 'petrol4ever', is_staff=True, is_superuser=True).save()

        if not (Session.objects.all()):
            return Response({'status': 'failed'})
        return Response({'status' : 'OK'})
            

class RefillSessions(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if not (Session.objects.all()):
            setUpSessions()
        else:
            return Response({'status': 'AlreadyFilled'})

        if not (Session.objects.all()):
            return Response({'status' : 'Failed'})
        return Response({'status':'SessionsFilled'})

class InspectUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)

        username = kwargs.get('username', None)

        if username:
            user = get_object_or_404(User, username=username)
            return Response(InspectUserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response({'status':'failed', 'message':'NoUserProvided'},status=status.HTTP_404_NOT_FOUND)


class UserMod(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(status=status.HTTP_404_NOT_FOUND)

        username = kwargs.get('username', None)
        password = kwargs.get('password', None)

        if (not username) or (not password):
            return Response({'message':'No username or password provided'},status=status.HTTP_404_NOT_FOUND)

        if User.objects.filter(username=username).exists():
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            return Response({'message':'Password successfully changed.'}, status=status.HTTP_200_OK)
        
        else:
            u = User.objects.create(username=username)
            u.set_password(password)
            u.save()
            return Response({'message':'User successfully created'}, status=status.HTTP_200_OK)

class SessionsUpd(APIView):

    def post(self, request):

        if not request.user.is_superuser:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        data = csv.DictReader(codecs.iterdecode(request.FILES['data_file'], 'utf-8'))
        # print(data)
        count_sessions = 0
        count_before = Session.objects.all().count()
        for row in data:
            count_sessions+=1
            try:
                provider =Provider.objects.get(id=row['ProviderID'])
                user = User.objects.get(id = row['UserID'])
                vehicle = Car.objects.get(id=row['VehicleID'])
                station = Station.objects.get(id=row['StationID'])
                point = Point.objects.get(id=row['PointID'])
                connectionTime = row['ConnectionTime']
                disconnectTime = row['DisconnectTime']
                doneChargingTime = row['DoneChargingTime']
                kWhDelivered = row['kWhDelivered']
                payment = row['Payment']
                s = Session.objects.filter(
                    customer=user,
                    vehicle=vehicle,
                    provider=provider,
                    station=station,
                    point=point,
                    payment=payment,
                    connectionTime=connectionTime,
                    disconnectTime=disconnectTime,
                    doneChargingTime=doneChargingTime,
                    kWhDelivered=kWhDelivered
                )
                if s:
                    continue
                session = Session.objects.create(
                    customer=user,
                    vehicle=vehicle,
                    provider=provider,
                    station=station,
                    point=point,
                    payment=payment,
                    connectionTime=connectionTime,
                    disconnectTime=disconnectTime,
                    doneChargingTime=doneChargingTime,
                    kWhDelivered=kWhDelivered
                )
                if payment == 'Credit':
                    is_paid=False
                else:
                    is_paid=True
                    Bill.objects.create(customer = user,
                                            date_created = connectionTime,
                                            total = session.price,
                                            is_paid = is_paid).save()
                if is_paid==False:
                    time = session.connectionTime
                    date = datetime.strptime(time,'%Y-%m-%d %H:%M:%S.00+00:00')
                    lastday = calendar.monthrange(date.year,date.month)[1]
                    start_date = datetime(date.year, date.month, 1).strftime('%Y-%m-%d')
                    end_date = datetime(date.year, date.month, lastday).strftime('%Y-%m-%d')
                    customer = user.customer
                    customer.has_expired_bills = True
                    customer.save()
                    m = MonthlyBill.objects.get_or_create(start_date = start_date, end_date = end_date , customer = user)
                    if m[1]:
                        m[0].save()
                    if m[0].monthly_total < 0:
                        m[0].monthly_total = session.price    
                    else:
                        m[0].monthly_total = m[0].monthly_total+session.price
                    m[0].save()
            except Exception as e:
                pass
        count_after = Session.objects.all().count()
        response = {
            "SessionsInUploadedFile":count_sessions, 
            "SessionsImported":count_after-count_before, 
            "TotalSessionsInDatabase":count_after
            }
        return Response(response, status=status.HTTP_200_OK)

 
class GetCars(APIView):
    permission_classes=(AllowAny,)

    def get(self,request):
        cars = CarBase.objects.all()
        
        serialized = CarSerializer(cars, many=True)

        return Response(serialized.data,status=status.HTTP_200_OK)

class MyCars(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        serializer = MyCarSerializer(request.user.cars,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class MyBills(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):

        serializer = BillSerializer(request.user.bills,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)

class MyMonthlyBills(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        
        serializer = MonthlyBillSerializer(request.user.monthlybills,many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ChargingSession(APIView):

    permission_classes = [IsAuthenticated]

    def post(sef, request):

        data = request.data
        try:
            provider = Provider.objects.get(id=int(data['ProviderID']))
            station = provider.providers.all().get(id=int(data['StationID']))
            point = station.comments.all().get(id=int(data['PointID']))
            user = request.user
            vehicle = user.cars.all().get(id=int(data['VehicleID']))
            if data['accharger']:

                charger = vehicle.car.ac_charger

            else:

                charger = vehicle.car.dc_charger

            charger.ports.all().get(id=int(data['PortID']))
        
        except Provider.DoesNotExist:
            return Response({'status':'Provider Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Station.DoesNotExist:
            return Response({'status':'Station Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Point.DoesNotExist:
            return Response({'status':'Point Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Car.DoesNotExist:
            return Response({'status':'Car Not Found'}, status=status.HTTP_404_NOT_FOUND)
        except Ports.DoesNotExist:
            return Response({'status':'Port is not Compatible'}, status=status.HTTP_404_NOT_FOUND)
     

        if data["kWh"]:
            kWhDelivered=data["kWhDelivered"]
        else:
            kWhDelivered=data["amount"]/provider.costPerkWh
        if vehicle.car.usable_battery_size <= float(kWhDelivered):
                kWhDelivered = vehicle.car.usable_battery_size

        session = Session.objects.create(
                    customer=user,
                    vehicle=vehicle,
                    provider=provider,
                    station=station,
                    point=point,
                    payment=data["payment"],
                    connectionTime=data["connectionTime"],
                    disconnectTime=data["disconnectTime"],
                    doneChargingTime=data["doneChargingTime"],
                    kWhDelivered=float(kWhDelivered)
                )

        if session.payment == 'Credit':
            is_paid=False
        else:
            is_paid=True
            Bill.objects.create(customer = user,
                                    date_created = session.connectionTime,
                                    total = session.price,
                                    is_paid = is_paid).save()
        if is_paid==False:
            time = session.connectionTime
            date = datetime.strptime(time,'%Y-%m-%d %H:%M:%S.00+00:00')
            lastday = calendar.monthrange(date.year,date.month)[1]
            start_date = datetime(date.year, date.month, 1).strftime('%Y-%m-%d')
            end_date = datetime(date.year, date.month, lastday).strftime('%Y-%m-%d')
            customer = user.customer
            customer.has_expired_bills = True
            customer.save()
            m = MonthlyBill.objects.get_or_create(start_date = start_date, end_date = end_date , customer = user)
            if m[1]:
                m[0].save()
            if m[0].monthly_total < 0:
                m[0].monthly_total = session.price    
            else:
                m[0].monthly_total = m[0].monthly_total+session.price
            m[0].save()
    
        return Response({'message':'Session created'},status=status.HTTP_200_OK)

class MonthlyPayoff(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        id = request.data["BillID"]
        

        monthly_bill = MonthlyBill.objects.get(id=id)
        if monthly_bill.monthly_total < 0:

            return Response({'status':'Monthly bill is already paid'}, status=status.HTTP_400_BAD_REQUEST)
        
        monthly_bill.payoff()

        return Response({'status':'Monthly bill is now paid'},status=status.HTTP_200_OK)

class getStations(APIView):

    permission_classes=(AllowAny,)
    authentication_classes = ()

    def get(self, request):

        stations = Station.objects.all()
        serializer = StationSerializer(stations, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)

class InsertCar(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:

            user = request.user

            car = CarBase.objects.get(id=request.data["CarID"])
            newCar = Car.objects.create(
                car = car,
                customer = user
                )
            newCar.save()

        except CarBase.DoesNotExist :

            return Response({'status':'Bad ID'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'status':'Created'},status=status.HTTP_200_OK)