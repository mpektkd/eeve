from django.db import models
from django.contrib.auth.models import User

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
    customer = models.ManyToManyField(User, related_name="monthlybills")
    monthly_total = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Monthly bill {self.start_date} to {self.end_date}."

 # Stored cards for customer
class Card(models.Model):
    customer = models.ForeignKey(User, related_name="cards", on_delete=models.CASCADE)
    card_no = models.IntegerField()

    def __str__(self):
        first_dig = self.card_no / 10000
        last_dig = self.card_no % 10000
        return f"{first_dig}********{last_dig}"

class Car(models.Model):
    CAR_TYPE = (
        ('BEV', 'Battery Electric Vehicle'),
        ('PHEV', 'Plug-in Hybrid Electric Vehicle'),
        ('HEV', 'Hybrid Electric Vehicle')
    )
    customer = models.ForeignKey(User, related_name="cars", on_delete=models.CASCADE)
    model = models.CharField()
    car_type = models.CharField(max_length=4, choices=CAR_TYPE)

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
        