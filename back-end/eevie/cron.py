from datetime import datetime, timedelta
from eevie.models import *
from django.contrib.auth.models import User
from pytz import timezone

def closeMonthlyBills():
    m = MonthlyBill.objects.all()
    now = datetime.datetime.now(timezone('Europe/Athens'))
    for bill in m:
        m.end_date = now - timedelta(days=1)
        newm = MonthlyBill.objects.create(
            customer = m.customer,
            monthly_total = 0,
            start_date = now, 
            end_date = None
        )
        newm.save()
        