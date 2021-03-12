from django.db import connection
from django.test import TestCase
from eevie.models import *
from django.contrib.auth.models import User
import pathlib
import json,datetime
from django.db.models import Count, Sum
from time import gmtime, strftime, localtime
from pytz import timezone
# Create your tests here.

class BrandsTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['brands']:
            b=Brands.create(**i)
            b.save()
        f.close()

    def test_brands(self):
        brand = Brands.objects.get(id='5663b87a-d940-4bab-9846-d74c8c0ae260')
        brandCount = Brands.objects.all().count()
        self.assertEqual(brand.name, "MG")
        self.assertEqual(brandCount,32)

class PortsTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['ConnectionTypes']:
            p = Ports.create(**i)
            p.save()
        f.close()

    def test_ports(self):
        port = Ports.objects.get(id=3)
        portCount = Ports.objects.all().count()
        self.assertEqual(port.title,"BS1363 3 Pin 13 Amp")
        self.assertEqual(portCount, 41)

class ACchargerTestCase(TestCase):
    def setUp(self):
        gpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        g = open(gpath)
        data = json.load(g)
        for i in data['ConnectionTypes']:
            p = Ports.create(**i)
            p.save()
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['data']:
            ac = ACcharger.create(**i['ac_charger'])
            ac.save()
        g.close()
        f.close()
    
    def test_ac(self):
        ac = ACcharger.objects.get(id=100)
        #print(ac.ports.all())

class DCchargerTestCase(TestCase):
    def setUp(self):
        gpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        g = open(gpath)
        data = json.load(g)
        for i in data['ConnectionTypes']:
            p = Ports.create(**i)
            p.save()
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['data']:
            if(i['dc_charger']==None):
                continue
            dc = DCcharger.create(**i['dc_charger'])
            dc.save()
        g.close()
        f.close()
    
    def test_dc(self):
        dc = DCcharger.objects.get(id=10)
        #print(dc.ports.all())

class CarBaseTestCase(TestCase):
    def setUp(self):
        brands = BrandsTestCase()
        brands.setUp()
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['data']:
            c=CarBase.create(**i)
            c.save()
        f.close()

    def test_cars(self):
        car = CarBase.objects.get(id='8b51a06f-676a-46aa-9074-4d3364ea1cca')
        #print(car)B
        carCount = CarBase.objects.all().count()

        #for i in car._meta.get_fields():
        #    print(type(i.name))
        #print(car.ac_charger)
        #print(car.dc_charger)
        self.assertEqual(car.type,"phev")
        self.assertEqual(carCount, 143)

class UsageTypeTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['UsageTypes']:
            u = UsageType.create(**i)
            u.save()
        f.close()
        
    def test_usage(self):
        #print(UsageType.objects.all())
        u = UsageType.objects.get(id = 7)
        self.assertEqual(u.IsAccessKeyRequired,False)

class StatusTypeTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['StatusTypes']:
            u = StatusType.create(**i)
            u.save()
        f.close()

    def test_status(self):
        s = StatusType.objects.get(id=75)
        self.assertEqual(s.IsOperational, True)
        s = StatusType.objects.get(id=210)
        self.assertEqual(s.IsOperational, False)

class AddressInfoTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json' #station_info_gr.json
        f = open(fpath)
        data = json.load(f)
        for i in data:
            a = AddressInfo.create(**i['AddressInfo'])
            if a != None:
                a.save()
        f.close()
    
    def test_address(self):
        s = AddressInfo.objects.get(id=172581)
        self.assertEqual(s.addressLine, '62 Μαρτύρων 506')
        #print(s)

class CurrentTypeTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['CurrentTypes']:
            c = CurrentType.create(**i)
            c.save()
        f.close()
    
    def test_current(self):
        c = CurrentType.objects.all()
        #print(c)

class CheckinStatusTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['CheckinStatusTypes']:
            cst = CheckinStatus.create(**i)
            cst.save()

    def test_cst(self):
        cst = CheckinStatus.objects.get(id=120)
        self.assertEqual(cst.title, 'Charging Spot Not Accessible (Access locked or site closed)')

class BillTestCase(TestCase):
    def setUp(self):
        Bill.objects.create(
            total=35.000,
            is_paid=True
        )

    def test_bills(self):
        b = Bill.objects.all()
        #print(b[0].date_created)

class StationTestCase(TestCase):
    def setUp(self):
        connectionTypes = PortsTestCase()
        connectionTypes.setUp()
        checkin = CheckinStatusTestCase()
        checkin.setUp()
        currentTypes = CurrentTypeTestCase()
        currentTypes.setUp()
        statusTypes = StatusTypeTestCase()
        statusTypes.setUp()
        usageTypes = UsageTypeTestCase()
        usageTypes.setUp()

        gpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json' #station_info_gr.json
        g = open(gpath)
        data = json.load(g)
        for i in data:
            st = Station.create(**i)
            if st != None:
                st.save()
        
    def test_stations(self):
        s = Station.objects.get(id= 108413)
        #print(s.usageCost)

class SessionsTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/providers.json'
        f = open(fpath)
        data = json.load(f)
        for i in data:
            p = Provider.objects.create(**i)
            p.save()

        stations = StationTestCase()
        stations.setUp()

        carBase = CarBaseTestCase()
        carBase.setUp()

        users = UsersTestCase()
        users.setUp()

        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/sessions2.json' #Data/sessions2.json
        f = open(fpath)
        data = json.load(f)
        for i in data["_items"]:
            s = Session.create(**i)
            s.save()
        
    def test_sessions(self):
        # print(Session.objects.all())
        date_from = '2019-9-01 16:56:18.00+00:00'
        date_to = '2020-8-03 22:02:13.00+00:00'

        try:

            # points = [Point.objects.get(id=263271)]
            # points = Point.objects.all()

            # for point in points:

            #     sessions = point.points.all().filter(connectionTime__range=[date_from,date_to])

            #     point_info = {}

            #     point_info['Point'] = point.id
            #     first = point.station.operators.all().first()
            #     if first is not None:
            #         point_info['PointOperator'] = first.title
            #     else:
            #         point_info['PointOperator'] = "Unknown"
            #     point_info['RequestTimesamp'] = datetime.datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
            #     point_info['PeriodFrom'] = date_from[:-9]
            #     point_info['PeriodTo'] = date_to[:-9]
            #     point_info['NumberOfChargingSessions'] = point.points.count()

            #     sessionslist = [] 
            #     index = 1
            #     for i in sessions:
            #         temp = {}
            #         temp['SessionIndex'] = index
            #         temp['SessionID'] = i.id
            #         temp['StartedOn'] = i.connectionTime.strftime("%Y-%m-%d %H:%M:%S")
            #         temp['FinishedOn'] = i.disconnectTime.strftime("%Y-%m-%d %H:%M:%S")
            #         temp['Protocol'] = i.point.protocol
            #         temp['EnergyDelivered'] = i.kWhDelivered
            #         temp['Payment'] = i.payment
            #         temp['VehicleType'] = i.vehicle.car.type
            #         index += 1
            #         sessionslist.append(temp.copy())

            #     point_info['ChargingSessionsList'] = sessionslist[:]

            #     print("----------------Info--------------------------")
            #     print(point_info)
            #     print(f"sessions: {sessions.count()}")


            stations = Station.objects.all()
            # stations = [Station.objects.get(id=172220)]
            for station in stations:

                sessions = station.sessions.all().filter(connectionTime__range=[date_from,date_to])
                
                station_info = {}
                station_info['StationID'] = station.id
                if station.operators.all().first() is not None:
                    station_info['Operator'] = station.operators.all().first().title
                else:
                    station_info['Operator'] = "Unknown"
                # station_info['RequestTimestamp'] = datetime.datetime.now(timezone('Europe/Athens'))
                station_info['RequestTimestamp'] = datetime.datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
                station_info['PeriodFrom'] = date_from
                station_info['PeriodTo'] = date_to
                station_info['TotalEnergyDelivered']=sessions.aggregate(Sum('kWhDelivered'))['kWhDelivered__sum']
                station_info['NumberOfChargingSessions'] = sessions.count()
                station_info['NumberOfActivePoints'] = len(sessions.values('point').annotate(Count('point__id')))
                station_info['SessionsSummaryList'] = list(sessions.values('point__id').annotate(PointSessions=Count('point'), EnergyDelivered = Sum('kWhDelivered')).order_by('-PointSessions'))
                print("----------------Info--------------------------")
                print(station_info)
                print(f"sessions: {sessions.count()}")
            # vehicles = [Car.objects.get(id=int(1))]
            # vehicles = Car.objects.all()

            # for vehicle in vehicles:
            #     sessions = vehicle.vehicle.all().filter(connectionTime__range=[date_from,date_to])

            #     ev_info = {}
            #     ev_info['VehicleID'] = vehicle.id
            #     ev_info['RequestTimestamp'] = datetime.datetime.now(timezone('Europe/Athens')).strftime("%Y-%m-%d %H:%M:%S")
            #     ev_info['PeriodFrom'] = date_from[:-9]
            #     ev_info['PeriodTo'] = date_to[:-9]
            #     kWh = sessions.aggregate(Sum('kWhDelivered'))['kWhDelivered__sum'] #average consumption ??
            #     if kWh is not None:
            #         ev_info['TotalEnergyConsumed']=kWh
            #     else:
            #         ev_info['TotalEnergyConsumed']=0
            #     ev_info['NumberOfVisitedPoints'] = len(sessions.values('point').annotate(Count('point__id')))
            #     ev_info['NumberOfVehicleChargingSessions'] = sessions.count()

            #     sessionslist = [] 
            #     index = 1
            #     for i in sessions:
            #         temp = {}
            #         temp['SessionIndex'] = index
            #         temp['SessionID'] = i.id
            #         temp['EnergyProvider'] = i.provider.name
            #         temp['StartedOn'] = i.connectionTime.strftime("%Y-%m-%d %H:%M:%S")
            #         temp['FinishedOn'] = i.disconnectTime.strftime("%Y-%m-%d %H:%M:%S")
            #         temp['EnergyDelivered'] = i.kWhDelivered
            #         temp['PricePolicyRef'] = i.payment
            #         temp['CostPerKWh'] = i.provider.costPerkWh
            #         temp['SessionCost'] = i.kWhDelivered*i.provider.costPerkWh
            #         index += 1
            #         sessionslist.append(temp.copy())

                
            #     ev_info['VehicleChargingSessionsList'] = sessionslist[:]
            #     print("----------------Info--------------------------")
            #     print(ev_info)
            #     print(f"sessions: {sessions.count()}")


            # # providers = [Provider.objects.get(id=int(1))]
            # providers = Provider.objects.all()

            # for provider in providers:

            #     sessions = provider.hasmade.all().filter(connectionTime__range=[date_from,date_to])

            #     provider_info = {}
            #     provider_info['ProviderID'] = provider.id
            #     provider_info['ProviderName'] = provider.name
            #     provider_info['CostPerKWh'] = provider.costPerkWh
                
            #     sessionslist = [] 
            #     for session in sessions:

            #         temp = {}
            #         temp['StationID'] = session.station.id
            #         temp['SessionID'] = session.id
            #         temp['VehicleID'] = session.vehicle.id
            #         temp['StartedOn'] = session.connectionTime.strftime("%Y-%m-%d %H:%M:%S")
            #         temp['FinishedOn'] = session.disconnectTime.strftime("%Y-%m-%d %H:%M:%S")
            #         temp['EnergyDelivered'] = session.kWhDelivered
            #         temp['PricePolicyRef'] = session.payment #have to change
            #         temp['TotalCost'] = session.kWhDelivered*provider.costPerkWh

            #         sessionslist.append(temp.copy())

            #     provider_info['ProviderChargingSessionsList'] = sessionslist[:]

            #     print("----------------Info--------------------------")
            #     print(provider_info)
            #     print(f"sessions: {sessions.count()}")

        except Exception as e:
            print('Not Found')
            return



class UsersTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/users.json'
        f = open(fpath)
        data = json.load(f)
        for i in data:
            u = User.objects.create(
                first_name = i['first_name'],
                last_name = i['last_name'],
                email = i['email'],
                username = i['username'],
                is_staff = i['is_staff'],
                is_active = i['is_active'],
                is_superuser = i['is_superuser'],
                last_login = i['last_login'],
                date_joined = i['date_joined']
            )
            u.set_password(i['password'])
            u.save()
            c = Customer.objects.create(
                user = u,
                has_expired_bills = False
            )
            c.save()
        
        Car.create()

    def test_users(self):
        u=User.objects.all().first()
        #print(u.id)