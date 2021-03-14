from rest_framework import serializers
from rest_framework import fields
from rest_framework.fields import ReadOnlyField
from rest_framework_jwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password
from eevie.models import *

class UserSerializer(serializers.ModelSerializer):
    apikey = ReadOnlyField(source='apikey.apikey')

    class Meta:
        model = User
        fields = ('id','username','apikey','password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()
        Customer.objects.create(user=instance,has_expired_bills=False)
        return instance

class InspectUserSerializer(serializers.ModelSerializer):
    apikey = ReadOnlyField(source='apikey.apikey')

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        token['username'] = user.username
        return token
    
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def get_user(self, obj):
       data =  UserSerializer(obj.user).data
       return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password')
        user = User(**user_data)

        if password is not None:
            user.set_password(password)
        user.save()
        customer = Customer.objects.create(user=user,**validated_data)
        customer.save()
        return customer

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer()
        super(CustomerSerializer,self).update(instance,validated_data)
        super(UserSerializer,user).update(instance.user,user_data)
        return instance

class BillSerializer(serializers.ModelSerializer):
    customer = ReadOnlyField(source='customer.id')

    class Meta:
        model=Bill
        fields='__all__'

class MonthlyBillSerializer(serializers.ModelSerializer):
    customer = ReadOnlyField(source='customer.id')

    class Meta:
        model=MonthlyBill
        fields='__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ['name']

class CarSerializer(serializers.ModelSerializer):
    brandName = ReadOnlyField(source='brand.name')

    class Meta:
        model = CarBase
        fields = '__all__'

class MyCarSerializer(serializers.ModelSerializer):
    car = CarSerializer()
    
    class Meta:
        model = Car
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressInfo
        fields = '__all__'

class ProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Provider
        fields = '__all__'

class PortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ports
        fields = '__all__'

class CurrentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CurrentType
        fields = '__all__'

class StatusTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = StatusType
        fields = '__all__'

class UsageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsageType
        fields = '__all__'

class PointSerializer(serializers.ModelSerializer):

    ports = PortSerializer(many=True)
    current_type = CurrentTypeSerializer(many=True)
    status_type = StatusTypeSerializer(many=True)

    class Meta:
        model = Point
        fields = '__all__'

class StationSerializer(serializers.ModelSerializer):

    addressInfo = AddressSerializer()
    providers = ProviderSerializer(many=True)
    comments = PointSerializer(many=True)
    comments.ports = PortSerializer(many=True)
    statusType = StatusTypeSerializer(many=True)
    usageType = UsageTypeSerializer(many=True)
    rating = ReadOnlyField()

    class Meta:
        model=Station
        fields=('__all__')
