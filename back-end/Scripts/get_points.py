from eevie.models import *

# stations = Station.objects.all()

# with open("points.txt", "w") as file:

#     for station in stations:
#         file.write(f"{station}\n\t")
#         # print(station.comments.all())
#         for point in station.comments.all():
#             file.write(f"{point}")
#             file.write("\t")
#         file.write("\n\n")

users = User.objects.all()

with open("vehicles.txt", "w") as file:

    for user in users:
        file.write(f"User: {user.username}\n\t")
        # print(station.comments.all())
        for car in user.cars.all():
            file.write(f"{car.car.dc_charger}")
            file.write("\t")
            file.write(f"{car.car.ac_charger}")
            file.write("\t")
        file.write("\n\n")

# bills = Bill.objects.all()

# with open("bills.txt", "w") as file:

#     for bill in bills:
#         file.write(f"{bill}\n\t")
#         # print(station.comments.all())
#         file.write("\n")
# bills = MonthlyBill.objects.all()

# with open("monthlybills.txt", "w") as file:

#     for bill in bills:
#         file.write(f"{bill}\n\t")
#         # print(station.comments.all())
#         file.write("\n")

# ports = Ports.objects.all()

# with open("Ports.txt", "w") as file:

#     for port in ports:
#         file.write(f"{port}\n\t")
#         # print(station.comments.all())
#         file.write("\n")

# chargers = ACcharger.objects.all()

# with open("acchargers.txt", "w") as file:

#     for charger in chargers:
#         file.write(f"{charger}\n\t")
#         # print(station.comments.all())
#         file.write("\n")


# chargers = DCcharger.objects.all()

# with open("dcchargers.txt", "w") as file:

#     for charger in chargers:
#         file.write(f"{charger}\n\t")
#         # print(station.comments.all())
#         file.write("\n")

# users = User.objects.all()

# with open("users.txt", "w") as file:

#     for user in users:
#         try:
#             file.write(f"{user.customer}\n\t")
#             # print(station.comments.all())
#             file.write("\n")
#         except:
#             pass


# cars = CarBase.objects.all()

# with open("carbase.txt", "w") as file:

#    for car in cars:
#         file.write(f"Car: {car.id}\n\t")
#         # print(station.comments.all())
#         for veh in car.carbase.all():
#             file.write(f"{veh.id}")
#             file.write("\t")
#         file.write("\n\n")