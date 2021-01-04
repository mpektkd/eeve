from django.db import models
from django.contrib.auth.models import User

 # Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_expired_bills = models.BooleanField()

    def __str__(self):
        return self.user.username

 # Individual Bill 
class Bill(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bills") # Many to One relationship with Customers
    date_created = models.DateTimeField(auto_now_add=True) # Updates automatically the time the object is saved
    total = models.FloatField()
    is_paid = models.BooleanField()

    def __str__(self):
        return f"Bill belongs to {self.customer.get_username()}."

 # Monthly Bill expires every 1st of month
class MonthlyBill(models.Model):
    customer = models.ManyToManyField(Customer, on_delete=models.CASCADE, related_name="monthlybills")
    monthly_total = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Monthly bill {self.start_date} to {self.end_date}."

 # Stored cards for customer
class Card(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="cards")
    card_no = models.IntegerField(max_length=16)

    def __str__(self):
        first_dig = self.card_no / 10000
        last_dig = self.card_no % 10000
        return f"{first_dig}********{last_dig}"

