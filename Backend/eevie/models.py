from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, DO_NOTHING, PROTECT
from django.db.models.fields import CharField, IntegerField, related
from django.core.validators import MaxValueValidator, RegexValidator
from django.utils import tree
import random

from . import validators

format_port = {
    "type2": "Type 2",
    "ccs": "CCS",
    "type1": "Type 1",
    "chademo": "CHAdeMO",
    "tesla_ccs": "CCS",
    "tesla_suc": "Tesla Supercharger"
}


 # Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_expired_bills = models.BooleanField()

    def __str__(self):
        return f"Customer with ID:{self.id} and username {self.user.get_username()}"

 # Individual Bill 
class Bill(models.Model):
    customer = models.ForeignKey(User, related_name="bills", on_delete=models.CASCADE, null=True) # Many to One relationship with Customers
    date_created = models.DateTimeField(auto_now_add=True) # Updates automatically the time the object is saved
    total = models.FloatField()
    is_paid = models.BooleanField()

    def __str__(self):
        return f"Bill with ID:{self.id} belongs to {self.customer.get_username()}."

 # Monthly Bill expires every 1st of month
class MonthlyBill(models.Model):
    customer = models.ForeignKey(User, related_name="monthlybills", on_delete=models.CASCADE, null=True) # Many to One relationship with Customers
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

 # To represent class Car

 # Filled by reference 
class Ports(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Port with ID: {self.id} and title {self.title}."

    @classmethod
    def create(cls, **kwargs):
        port = cls.objects.create(
            id=kwargs['ID'],
            title=kwargs['Title']
        )
        return port

# Filled by reference
class Brands(models.Model):
    id = models.CharField(max_length=100 ,primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"Brand {self.name} has ID: {self.id}."

    @classmethod
    def create(cls, **kwargs):
        brand = cls.objects.create(
            id = kwargs['id'],
            name = kwargs['name']
        )
        return brand

# Filled by model car
class ACcharger(models.Model):
    id = models.AutoField(primary_key=True)
    usable_phases = models.IntegerField()
    ports = models.ManyToManyField(Ports, related_name='portas') # Many to Many relationship to existing Ports
    max_power = models.FloatField()
    # Might want to insert power_per_charging_point afterwards

    def __str__(self):
        return f"AC charger with {self.usable_phases} phases, available ports: {self.ports.all()} and {self.max_power} max power."

 # kwargs is data['data']['ac_charger']
    @classmethod
    def create(cls,**kwargs):
        charger = cls.objects.create(
            usable_phases = kwargs['usable_phases'],
            max_power = kwargs['max_power']
        )
        for i in kwargs['ports']:
            formatted_port = format_port[i]
            #print(formatted_port)
            port = Ports.objects.filter(title__startswith=formatted_port)
            for portinstance in port:
                #print(portinstance)
                charger.ports.add(portinstance)
        #print(charger.ports)
        return charger

class chargingCurve(models.Model):
    id = models.AutoField(primary_key=True)
    percentage = models.FloatField(validators=[validators.validate_percentage])
    power = models.FloatField()

    def __str__(self):
        return f"Charging percentage {self.percentage} with power {self.power}."

class DCcharger(models.Model):
    id = models.AutoField(primary_key=True)
    ports = models.ManyToManyField(Ports) # Many to Many relationship to existing Ports
    max_power = models.FloatField()
    charging_curve = models.ManyToManyField(chargingCurve)

    def __str__(self):
        return f"DC charger with available ports: {self.ports.all()} and {self.charging_curve.all()}."

# kwargs is data['data']['dc_charger']
    @classmethod
    def create(cls,**kwargs):
        dcharger= cls.objects.create(
            max_power = kwargs['max_power']
        )
        for i in kwargs['ports']:
            formatted_port = format_port[i]
            port = Ports.objects.filter(title__startswith=f"{formatted_port}")
            for portinstance in port:
                dcharger.ports.add(portinstance)
        
        for i in kwargs['charging_curve']:
            curve = chargingCurve.objects.get_or_create(
                percentage=i['percentage'],
                power=i['power']
            )
            dcharger.charging_curve.add(curve[0])
        
        return dcharger

class Car(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    type = models.CharField(max_length=4, null=True)
    brand = models.ForeignKey(Brands, on_delete=PROTECT, null=True)
    model = models.CharField(max_length=100)
    release_year = models.IntegerField(validators=[validators.validate_year],null=True)
    usable_battery_size = models.FloatField(validators=[validators.validate_percentage])
    ac_charger = models.OneToOneField(ACcharger, on_delete=PROTECT, null=True)
    dc_charger = models.OneToOneField(DCcharger, on_delete=PROTECT, null=True)
    average_consumption = models.FloatField(validators=[validators.validate_percentage])
    customer = models.ForeignKey(User, related_name="cars", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"Car with ID: {self.id},model {self.model} and type {self.type}."

 # kwargs is data['data']
    @classmethod
    def create(cls,**kwargs):
        car = cls.objects.create(
            id = kwargs['id'],
            type = kwargs['type'],
            model = kwargs['model'],
            release_year = kwargs['release_year'],
            usable_battery_size = kwargs['usable_battery_size'],
            average_consumption = kwargs['energy_consumption']['average_consumption']
        )
        brand_id = kwargs['brand_id']
        brand_to_enter = Brands.objects.get(id=brand_id)
        car.brand = brand_to_enter
        ac_charger = ACcharger.create(**kwargs['ac_charger'])
        #print(ac_charger)
        car.ac_charger=ac_charger
        if kwargs['dc_charger'] != None:
            dc_charger = DCcharger.create(**kwargs['dc_charger'])
            car.dc_charger = dc_charger
        
        return car
 
# To reprsent class Station
class Operator(models.Model):
    id = models.IntegerField(primary_key=True)
    website_url = models.URLField(null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Operator {self.title}, website {self.website_url}, email {self.contact_email}."

# Filled by reference
class UsageType(models.Model):
    id = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=100)
    IsPayAtLocation = models.BooleanField(null=True, blank=True)
    IsMembershipRequired = models.BooleanField(null=True, blank=True)
    IsAccessKeyRequired = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Is {self.Title} with ID: {self.id}, IsPayAtLocation:{self.IsPayAtLocation}, IsMembershipRequired:{self.IsMembershipRequired}, IsAccessKeyRequired:{self.IsAccessKeyRequired}.\n"

 # kwargs is data['UsageTypes']
    @classmethod
    def create(cls,**kwargs):
        usagetype = cls.objects.create(
            id = kwargs['ID'],
            Title = kwargs['Title'],
            IsPayAtLocation = kwargs['IsPayAtLocation'],
            IsMembershipRequired = kwargs['IsMembershipRequired'],
            IsAccessKeyRequired = kwargs['IsAccessKeyRequired']
        )
        return usagetype
    
 # Filled by reference
class StatusType(models.Model):
    id = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=100)
    IsOperational = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"Is {self.Title}"

 # kwargs is data['StatusTypes']
    @classmethod
    def create(cls,**kwargs):
        status = cls.objects.create(
            id = kwargs['ID'],
            Title = kwargs['Title'],
            IsOperational = kwargs['IsOperational']
        )
        return status

 # Filled by station.create
class AddressInfo(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    addressLine = models.CharField(max_length=100)
    town = models.CharField(max_length=100, null=True)
    stateOrProvince = models.CharField(max_length=100, null=True)
    postCode = models.CharField(max_length=10,null=True)
    countryId = models.IntegerField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longtitude = models.DecimalField(max_digits=9, decimal_places=6)
    contact_telephone = models.CharField(max_length=13, null=True, blank=True)
    access_comments = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.addressLine}, {self.town}, {self.postCode}."

 # kwargs is data['AddressInfo']
    @classmethod
    def create(cls,**kwargs):
        check = AddressInfo.objects.filter(id = kwargs['ID'])
        if check:
            return None
        address = cls.objects.create(
            id = kwargs['ID'],
            title = kwargs['Title'],
            addressLine = kwargs['AddressLine1'],
            town = kwargs['Town'],
            stateOrProvince = kwargs['StateOrProvince'],
            postCode = kwargs['Postcode'],
            countryId = kwargs['CountryID'],
            latitude = kwargs['Latitude'],
            longtitude = kwargs['Longitude'],
            contact_telephone = kwargs['ContactTelephone1'],
            access_comments = kwargs['AccessComments']
        )
        return address

 # Filled by reference
class CurrentType(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"Current type of {self.title} and id {self.id}."

 # kwargs is data['CurrentTypes']
    @classmethod
    def create(cls,**kwargs):
        currType = cls.objects.create(
            id = kwargs['ID'],
            title = kwargs['Title']
        )
        return currType

 # Filled by stations.create
class Connections(models.Model):
    id = models.IntegerField(primary_key=True)
    ports = models.ManyToManyField(Ports, related_name="exist_at")
    current_type = models.ManyToManyField(CurrentType, related_name="exists_at",blank=True)
    voltage = models.IntegerField(null=True, blank=True)
    powerKW = models.FloatField(null=True)
    quantity = models.IntegerField(null=True)
    status_type = models.ManyToManyField(StatusType, blank=True) #One status type to many connections

    def __str__(self):
        return f"{self.quantity} connections with ports {self.ports.all()} and current type {self.current_type.all()}."
     

class Provider(models.Model):
    id = models.AutoField(primary_key=True)
    costPerkWh = models.FloatField()
    name = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} provider with cost per kWh {self.costPerkWh}"

    @classmethod
    def create(cls, **kwargs):
        provider = cls.objects.create(
            costPerkWh = kwargs['costPerkWh'],
            name = kwargs['name']
        )
        provider.save()
        return provider
    

class Station(models.Model):
    id = models.IntegerField(primary_key=True)
    providers = models.ManyToManyField(Provider, related_name="providers")
    operators = models.ManyToManyField(Operator, related_name="operates")
    connections = models.ManyToManyField(Connections)
    usageType = models.ManyToManyField(UsageType, blank=True)
    statusType = models.ManyToManyField(StatusType, blank=True)
    addressInfo = models.OneToOneField(AddressInfo,related_name="belongs_to",on_delete=models.CASCADE, null=True)
    usageCost = models.CharField(null=True, blank=True, max_length=100)
    #userComments in UserComments table, accessed by station.UserComments
    generalComments = models.CharField(max_length=1000, null=True, blank=True) 
    
    def __str__(self):
        return f"Station with  {self.connections.all()} at {self.addressInfo}."

# kwargs is data
    @classmethod
    def create(cls,**kwargs):
        check = Station.objects.filter(id = kwargs['ID'])
        if check:
            return None

        station = cls.objects.create(
            id = kwargs['ID'],
            generalComments = kwargs['GeneralComments'],
            usageCost = kwargs['UsageCost'])

        opInfo = kwargs['OperatorInfo']
        if opInfo != None:
            operator = Operator.objects.get_or_create(
                id = opInfo['ID'],
                website_url = opInfo['WebsiteURL'],
                contact_email = opInfo['ContactEmail'],
                title = opInfo['Title']
            )
            if operator[1]:
                operator[0].save
            station.operators.add(operator[0])
        
        connectionsInfo = kwargs['Connections']
        for i in connectionsInfo:
            connectiona = Connections.objects.get_or_create(
                id = i['ID'],
                voltage = i['Voltage'],
                powerKW = i['PowerKW'],
                quantity = i['Quantity']
            )

            connection = connectiona[0]
            port = Ports.objects.get(id=i['ConnectionTypeID'])
            #print(port)
            connection.ports.add(port)
            if i['CurrentTypeID'] != None:
                currType = CurrentType.objects.get(id=i['CurrentTypeID'])
                connection.current_type.add(currType)

            if i['StatusTypeID'] != None:
                status = StatusType.objects.get(id=i['StatusTypeID'])
                connection.status_type.add(status)

            if connectiona[1]:
                connection.save()
            #print(connection)
            station.connections.add(connection)
        
        if kwargs['UsageTypeID'] != None:
            usagetype = UsageType.objects.get(id=kwargs['UsageTypeID'])
            station.usageType.add(usagetype)
        
        if kwargs['StatusTypeID'] != None:
            statustype = StatusType.objects.get(id=kwargs['StatusTypeID'])
            station.statusType.add(statustype)

        addressInfo = AddressInfo.create(**kwargs['AddressInfo'])
        if addressInfo != None:
                addressInfo.save()
        
        station.addressInfo = addressInfo

        if kwargs['UserComments'] != None:
            for i in kwargs['UserComments']:
                ucomm = UserComments.objects.create(
                    station = station,
                    username = i['UserName'],
                    comment = i['Comment'],
                    rating = i['Rating'],
                )
                if i['CheckinStatusTypeID'] != None:
                    ucomm.checkinStatus.add(CheckinStatus.objects.get(id=i['CheckinStatusTypeID']))
        
        if kwargs['MediaItems'] != None:
            for i in kwargs['MediaItems']:
                m = station.mediaItems.get_or_create(
                    id = i['ID'],
                    itemUrl = i['ItemURL'],
                )
                if m[1]:
                    m[0].save()

        return station

    @property
    def rating(self):
        count=0
        rating=0
        allComms = UserComments.objects.select_related('rating').filter(station__id=self.id)
        
        for i in allComms:
            if i.rating != None:
                rating += i.rating
                count += 1
        
        return rating/count

 # Filled by stations.create
class MediaTypes(models.Model):
    id = models.IntegerField(primary_key=True)
    itemUrl = models.URLField(null=True)
    station = models.ForeignKey(Station, related_name="mediaItems", on_delete=models.CASCADE)

    def __str__(self):
        return f"Media ID: {self.id} and URL: {self.itemUrl} and station {self.station}."

 # Filled by reference
class CheckinStatus(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"Checkin status {self.title} with ID: {self.id}."

# kwargs is data['CheckinStatusTypes']
    @classmethod
    def create(cls, **kwargs):
        checkin = cls.objects.create(
            id = kwargs['ID'],
            title = kwargs['Title']
        )
        return checkin

class UserComments(models.Model):
    id = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, related_name="UserComments", on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)
    customer = models.ForeignKey(User, related_name="myComments",on_delete=models.CASCADE, null=True, blank=True)
    checkinStatus = models.ManyToManyField(CheckinStatus)

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    provider = models.OneToOneField(Provider, related_name="hasmade", on_delete=models.DO_NOTHING, null=True)
    customer = models.ForeignKey(User, related_name="sessions", on_delete=models.CASCADE)  
    station = models.OneToOneField(Station, related_name="sessions", on_delete=models.CASCADE, null=True)
    connectionTime = models.DateTimeField(null=True)
    disconnectTime = models.DateTimeField(null=True)
    doneChargingTime = models.DateTimeField(null=True)
    kWhDelivered = models.FloatField(null=True)
    
    def __str__(self):
        return f"Charged with {self.provider.get_provider_display} for {self.duration}, transfered totally {self.total_kwh} KWh for {self.cost} euros."
    
    @classmethod
    def create(cls, **kwargs):
        users = User.objects.all()
        random_user = random.choice(users)
        providers = Provider.objects.all()
        random_provider = random.choice(providers)
        stations = Station.objects.all()
        random_station = random.choice(stations)

        session = cls.objects.create(
            customer = random_user,
            provider = random_provider,
            station = random_station,
            connectionTime = kwargs['connectionTime'],
            disconnectTime = kwargs['disconnectTime'],
            doneChargingTime = kwargs['doneChargingTime'],
            kWhDelivered = kwargs['kWhDelivered']
        )

        for i in kwargs['userInput']:
            user_inputs = UserInput.create(**i)
            user_inputs.save()
        session.userInputs.add(user_inputs)
        return session
        
class UserInput(models.Model):
    session = models.ForeignKey(Session, related_name="userInputs", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name="inputs", on_delete=models.CASCADE)
    WhPerMile = models.IntegerField(null=True)
    kWhRequested = models.FloatField(null=True)
    milesRequested = models.IntegerField(null=True)
    minutesAvailable = models.IntegerField(null=True)
    modifiedAt = models.DateTimeField(null=True)
    requestedDeparture = models.DateTimeField(null=True)

    def __str__(self):
        return f"User {self.customer.username} requested {self.kWhRequested} kWh, {self.milesRequested} miles for a car with consumption {self.WhPerMile} Wh/mile. He requested departure at {self.requestedDeparture} minutes from {self.modifiedAt} and has {self.minutesAvailable}."

    @classmethod
    def create(cls, **kwargs):
        userInput = cls.objects.create(
            WhPerMile = kwargs['WhPerMile'],
            kWhRequested = kwargs['kWhRequested'],
            milesRequested = kwargs['milesRequested'],
            minutesAvailable = kwargs['minutesAvailable'],
            modifiedAt = kwargs['modifiedAt'],
            requestedDeparture = kwargs['requestedDeparture']
        )

        return userInput