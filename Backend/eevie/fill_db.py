import django
import pathlib
import json,datetime
from eevie.models import *
from django.contrib.auth.models import User

def setUpBrands():
        fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
        f = open(fpath)
        data = json.load(f)
        for i in data['brands']:
            b=Brands.create(**i)
            b.save()
        f.close()

def setUpCurrentType():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['CurrentTypes']:
        c = CurrentType.create(**i)
        c.save()
    f.close()


def setUpPorts():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['ConnectionTypes']:
        p = Ports.create(**i)
        p.save()
    f.close()


def setUpAC():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['data']:
        ac = ACcharger.create(**i['ac_charger'])
        ac.save()

def setUpDC():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['data']:
        if(i['dc_charger']==None):
            continue
        dc = DCcharger.create(**i['dc_charger'])
        dc.save()
    f.close()

def setUpCarBase():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/electric_vehicles_data.json' #electric_vehicles_data.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['data']:
        c=CarBase.create(**i)
        c.save()
    f.close()


def setUpUsageTypes():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['UsageTypes']:
        u = UsageType.create(**i)
        u.save()
    f.close()

def setUpStatusTypes():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['StatusTypes']:
        u = StatusType.create(**i)
        u.save()
    f.close()

# def setUpAddressInfo():
#     fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json' #station_info_gr.json
#     f = open(fpath)
#     data = json.load(f)
#     for i in data:
#         a = AddressInfo.create(**i['AddressInfo'])
#         if a != None:
#             a.save()
#     f.close()

def setUpCheckinStatus():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/reference2.json'
    f = open(fpath)
    data = json.load(f)
    for i in data['CheckinStatusTypes']:
        cst = CheckinStatus.create(**i)
        cst.save()
    f.close()

def setUpProviders():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/providers.json'
    f = open(fpath)
    data = json.load(f)
    for i in data:
        p = Provider.objects.create(**i)
        p.save()
    f.close()

def setUpStation():
    gpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/station_info_gr.json' #station_info_gr.json
    g = open(gpath)
    data = json.load(g)
    for i in data:
        st = Station.create(**i)
        if st != None:
            st.save()
    g.close()


def setUpUsers():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/userslarge.json'
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

def setUpSessions():
    fpath = pathlib.Path(__file__).parent.parent.absolute() / 'Data/sessions2.json' #Data/sessions2.json
    f = open(fpath)
    data = json.load(f)
    for i in data["_items"]:
        s = Session.create(**i)
        s.save()
    f.close()


# setUpBrands()
# setUpCurrentType()
# setUpPorts()
# setUpAC()
# setUpDC()
# setUpCarBase()
# setUpUsageTypes()
# setUpStatusTypes()
# # setUpAddressInfo()
# setUpCheckinStatus()
# setUpUsers()
# setUpProviders()
# setUpStation()
# setUpSessions()