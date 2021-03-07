from eevie.models import *
from django.contrib.auth.models import User
import pathlib
import json,datetime

def setUpBrands(self):
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['brands']:
            b=Brands.create(**i)
            b.save()
        f.close()

def setUpCurrentType(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['CurrentTypes']:
        c = CurrentType.create(**i)
        c.save()
    f.close()


def setUpPorts(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['ConnectionTypes']:
        p = Ports.create(**i)
        p.save()
    f.close()


def setUpAC(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['data']:
        ac = ACcharger.create(**i['ac_charger'])
        ac.save()

def setUpDC(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['data']:
        if(i['dc_charger']==None):
            continue
        dc = DCcharger.create(**i['dc_charger'])
        dc.save()
    f.close()

def setUpCarBase(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['data']:
        c=CarBase.create(**i)
        c.save()
    f.close()


def setUpUsageTypes(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['UsageTypes']:
        u = UsageType.create(**i)
        u.save()
    f.close()

def setUpStatusTypes(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['StatusTypes']:
        u = StatusType.create(**i)
        u.save()
    f.close()

def setUpAddressInfo(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json' #station_info_gr.json
    f = open(fpath)
    data = json.load(f)
    for i in data:
        a = AddressInfo.create(**i['AddressInfo'])
        if a != None:
            a.save()
    f.close()

def setUpCheckinStatus(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['CheckinStatusTypes']:
        cst = CheckinStatus.create(**i)
        cst.save()
    f.close()

def setUpStation(self):
    gpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json' #station_info_gr.json
    g = open(gpath)
    data = json.load(g)
    for i in data:
        st = Station.create(**i)
        if st != None:
            st.save()
    g.close()


def setUpUsers(self):
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

def setUpSessions(self):
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/sessions2.json' #Data/sessions2.json
    f = open(fpath)
    data = json.load(f)
    for i in data["_items"]:
        s = Session.create(**i)
        s.save()
    f.close()