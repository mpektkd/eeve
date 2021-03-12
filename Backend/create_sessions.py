from eevie.models import *
import csv
import time

def str_time_prop(start, end, format, prop):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, "%Y-%m-%d %I:%M:%S.00+00:00", prop)


PAYMENT_OPTIONS = ['Cash','Debit Card','Credit']

rand = random.random
date_start = "2019-1-01 01:01:01.00+00:00"
date_end = "2021-3-05 01:01:01.00+00:00"
providers = Provider.objects.all()
users = User.objects.all()
number_of_sessions = 3
with open('data_file.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ProviderID", "UserID","VehicleID","StationID","PointID","ConnectionTime","DisconnectTime","DoneChargingTime","kWhDelivered","Payment"])
    
    for i in range(number_of_sessions):

        provider = random.choice(providers)
        station = random.choice(provider.providers.all())
        point = random.choice(station.comments.all())
        user = random.choice(users)
        car = random.choice(user.cars.all())
        connectionTime = random_date(date_start, date_end, random.random())[:]
        b = datetime.strptime(connectionTime, "%Y-%m-%d %I:%M:%S.00+00:00")
        c = datetime(b.year, b.month, b.day, (b.hour+(int(rand()*10)))%24, (b.minute+(int(rand()*10)))%60, (b.second+(int(rand()*10)))%60, (b.microsecond+(int(rand()*10)))%100)
        c = c.strftime("%Y-%m-%d %I:%M:%S.00+00:00")
        doneCharginTime = c[:]
        b = datetime.strptime(doneCharginTime, "%Y-%m-%d %I:%M:%S.00+00:00")
        c = datetime(b.year, b.month, b.day, (b.hour+(int(rand()*10)))%24, (b.minute+(int(rand()*10)))%60, (b.second+(int(rand()*10)))%60, (b.microsecond+(int(rand()*10)))%100)
        c = c.strftime("%Y-%m-%d %I:%M:%S.00+00:00")
        disconnecTime = c[:]
        kWhDelivered = rand()*100
        payment = random.choice(PAYMENT_OPTIONS)
        writer.writerow([provider.id, user.id, car.id, station.id, point.id, connectionTime, disconnecTime, doneCharginTime, kWhDelivered, payment])