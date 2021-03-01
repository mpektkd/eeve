from django.test import TestCase
from eevie.models import *
from django.contrib.auth.models import User
import pathlib
import json

# Create your tests here.

class BrandsTestCase(TestCase):
    def setUp(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json'
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
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json'
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
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json'
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

class CarTestCase(TestCase):
    def setUp(self):
        gpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        g = open(gpath)
        data = json.load(g)
        for i in data['ConnectionTypes']:
            p = Ports.create(**i)
            p.save()
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json'
        f = open(fpath)
        data = json.load(f)
        for j in data['brands']:
            b=Brands.create(**j)
            b.save()
        for i in data['data']:
            c=Car.create(**i)
            c.save()
        f.close()
        g.close()

    def test_cars(self):
        car = Car.objects.get(id='8b51a06f-676a-46aa-9074-4d3364ea1cca')
        #print(car)
        carCount = Car.objects.all().count()

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
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json'
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
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['ConnectionTypes']:
            p = Ports.create(**i)
            p.save()
        for i in data['CheckinStatusTypes']:
            cst = CheckinStatus.create(**i)
            cst.save()

        for i in data['CurrentTypes']:
            c = CurrentType.create(**i)
            c.save()
        
        for i in data['StatusTypes']:
            s = StatusType.create(**i)
            s.save()

        for i in data['UsageTypes']:
            u = UsageType.create(**i)
            u.save()
        gpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json'
        g = open(gpath)
        data = json.load(g)
        for i in data:
            st = Station.create(**i)
            if st != None:
                st.save()
        
    def test_stations(self):
        s = Station.objects.get(id= 108413)
        #print(s.usageCost)

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

    def test_users(self):
        u=User.objects.get(first_name = 'Lorne')
        #print(u.id)
        print(u.password)
        self.assertEqual(u.email,'lwooffinden0@dmoz.org')
        c = Customer.objects.get(user__username = 'lcowherdb2')
        self.assertEqual(c.user.first_name, 'Lily')