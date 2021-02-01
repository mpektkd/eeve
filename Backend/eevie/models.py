from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField

from . import validators

 # Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_expired_bills = models.BooleanField()

    def __str__(self):
        return f"Customer with ID:{self.id} and username {self.user.getusername()}"

 # Individual Bill 
class Bill(models.Model):
    customer = models.ForeignKey(User, related_name="bills", on_delete=models.CASCADE) # Many to One relationship with Customers
    date_created = models.DateTimeField(auto_now_add=True) # Updates automatically the time the object is saved
    total = models.FloatField()
    is_paid = models.BooleanField()

    def __str__(self):
        return f"Bill with ID:{self.id} belongs to {self.customer.get_username()}."

 # Monthly Bill expires every 1st of month
class MonthlyBill(models.Model):
    customer = models.ForeignKey(User, related_name="monthlybills", on_delete=models.CASCADE) # Many to One relationship with Customers
    monthly_total = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Monthly bill {self.start_date} to {self.end_date}."

 # Stored cards for customer
class Card(models.Model):
    customer = models.ForeignKey(User, related_name="cards", on_delete=models.CASCADE) # Many to One relationship with Customers
    card_no = models.IntegerField()

    def __str__(self):
        first_dig = self.card_no / 10000
        last_dig = self.card_no % 10000
        return f"{first_dig}********{last_dig}"


class Ports(models.Model):
    id = models.IntegerField()
    title = models.CharField()

    def __str__(self):
        return f"Port with ID: {self.id} and title {self.title}."

class Brands(models.Model):
    id = models.CharField()
    name = models.CharField()

    def __str__(self):
        return f"Brand {self.name} has ID: {self.id}."

class ACcharger(models.Model):
    usable_phases = models.IntegerField()
    ports = models.ManyToManyField(Ports, on_delete=models.DO_NOTHING) # Many to Many relationship to existing Ports
    max_power = models.FloatField()
    # Might want to insert power_per_charging_point afterwards

    def __str__(self):
        return f"AC charger with {self.usable_phases} phases, available ports: {self.ports} and {self.max_power} max power."

class chargingCurve(models.Model):
    percentage = models.FloatField(validators=[validators.validate_percentage])
    power = models.FloatField()

    def __str__(self):
        return f"Charging percentage {self.percentage} with power {self.power}."

class DCcharger(models.Model):
    ports = models.ManyToManyField(Ports, on_delete=models.DO_NOTHING) # Many to Many relationship to existing Ports
    max_power = models.FloatField()
    charging_curve = models.ManyToManyField(chargingCurve, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"DC charger with available ports: {self.ports}."

class Car(models.Model):
    id = models.CharField()
    brand = models.OneToOneField(Brands, on_delete=models.DO_NOTHING)
    model = models.CharField()
    release_year = models.IntegerField(validators=[validators.validate_year])
    usable_battery_size = models.FloatField(validators=[validators.validate_percentage])
    ac_charger = models.OneToOneField(ACcharger, on_delete=models.DO_NOTHING)
    dc_charger = models.OneToOneField(DCcharger, on_delete=models.DO_NOTHING)
    average_consumption = models.FloatField(validators=[validators.validate_percentage])
    customer = models.ForeignKey(User, related_name="cars", on_delete=models.CASCADE)

    def __str__(self):
        return f"Car with ID: {self.id},model {self.model} and type {self.get_car_type_display()} belongs to {self.customer.get_username()}."

class Session(models.Model):
    customer = models.ForeignKey(User, related_name="sesh", on_delete=models.CASCADE)
    #provider = models.CharField(max_length=1, choices=PROVIDERS)
    duration = models.TimeField()
    total_kwh = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return f"Charged with {self.provider.get_provider_display} for {self.duration}, transfered totally {self.total_kwh} KWh for {self.cost} euros."

class Providers(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return f"Provider is: {self.name}."

class Station(models.Model):
    # To implement location and rating
    providers = models.ManyToManyField(Providers, related_name="providers")
    # To implement __str__ to display location and rating

class Docks(models.Model):
    dock_type = models.CharField(max_length=15)

    def __str__(self):
        return self.dock_type
        