from rest_framework import serializers
from eevie.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    unique=True
    class Meta:
        model = Customer
        fields = '__all__'
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_user(self, obj):
       data =  UserSerializer(obj.user).data
       return data
    