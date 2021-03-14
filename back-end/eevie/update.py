from eevie.models import *
# import json

# f = open('Data/station_info_gr.json', 'r')
# data = json.load(f)

# for i in data:
#     Station.update(**i)


users = User.objects.all()

for user in users:

    sessions = user.sessions.all()
    bills = user.bills.all()

    for session, bill in zip(sessions,bills):

        print(bill, session)
        # bill.date_created = session.connectionTime
        # bill.total = session.kWhDelivered*session.provider.costPerkWh

        # if session.payment == "Credit":

        #     bill.is_paid = False
        
        # bill.save()
