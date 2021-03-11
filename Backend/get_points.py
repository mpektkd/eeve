from eevie.models import *

stations = Station.objects.all()

with open("points.txt", "w") as file:

    for station in stations:
        file.write(f"{station}\n\t")
        # print(station.points.all())
        for point in station.points.all():
            file.write(f"{point}")
            file.write("\t")
        file.write("\n\n")

# users = [User.objects.get(id=71)]
users = User.objects.all()

with open("vehicles.txt", "w") as file:

    for user in users:
        file.write(f"User: {user.username}\n\t")
        # print(station.points.all())
        for car in user.cars.all():
            file.write(f"{car.car.id}")
            file.write("\t")
        file.write("\n\n")

# cars = CarBase.objects.all()

# with open("carbase.txt", "w") as file:

#    for car in cars:
#         file.write(f"Car: {car.id}\n\t")
#         # print(station.points.all())
#         for veh in car.carbase.all():
#             file.write(f"{veh.id}")
#             file.write("\t")
#         file.write("\n\n")