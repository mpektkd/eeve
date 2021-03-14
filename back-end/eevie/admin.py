from django.contrib import admin

from .models import *
# Register your models here.

from django.contrib import admin
from eevie.models import *

@admin.register(Customer,Bill,MonthlyBill,
                Card,Brands,Ports,ACcharger,
                chargingCurve,DCcharger,CarBase,
                Car,Operator,UsageType,StatusType,
                AddressInfo,CurrentType,Provider,
                Station,Point,MediaTypes,CheckinStatus,
                UserComments,Session,UserInput)
                
class PersonAdmin(admin.ModelAdmin):
    pass
