from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication,SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from eevie.serializers import *
from eevie.models import *
# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    
    serializer_class = UserSerializer
    queryset = User.objects.all()   
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()   
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]