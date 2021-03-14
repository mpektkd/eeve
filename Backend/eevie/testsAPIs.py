from django.db.models.query import QuerySet
from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.urls import reverse
from eevie.models import *
from eevie.views import *
from eevie.tests import ReferenceTest,SessionsTestCase

class UserInterferenceTest(APITestCase):
    def test_user_interference(self):

        ReferenceTest().setUp()
        
        # Test Signup
        url = reverse('signup')
        user_data = {'username' : 'KiriakosM', 'password' : 'eimaiokalyterosprwthypourgos', 'car_id' : '27d7610e-9a77-498a-b1b5-28d4bc92cbf2'}
        response = self.client.post(url,user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(),1)
        
        # Test Login
        url = reverse('token_create')
        data = {'username' : 'KiriakosM', 'password' : 'eimaiokalyterosprwthypourgos'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data
        authorize = 'JWT ' + token['access']

        # Test current user 
        url = reverse('current_user')
        response = self.client.get(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.data,{'id':1, 'username':'KiriakosM'})

        # Test add car
        url = reverse('addcar')
        data = {"CarID" : 'a9a177bf-9ce5-4b67-b3ef-51af248b48c2'}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Created')

        # Test mycars
        url = reverse('mycars')
        response = self.client.get(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), User.objects.get(username='KiriakosM').cars.all().count())

        # Test sessions
        point = Station.objects.get(id=172220).comments.all().first()

        url = reverse('mychargingsession')
        data = {
            "ProviderID":str(Station.objects.get(id=172220).providers.all().first().id),
            "StationID":"172220",
            "PointID":str(point.id),
            "PortID":str(point.ports.all().first().id),
            "VehicleID":"2",
            "kWh":True,
            "accharger":False,
            "kWhDelivered":23.3,
            "amount":'null',
            "connectionTime":"2019-09-12 10:41:10.00+00:00",
            "disconnectTime":"2020-09-12 12:41:10.00+00:00",
            "doneChargingTime":"2019-09-12 11:41:10.00+00:00",
            "payment":"Cash"
        }

        response = self.client.post(url, data, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Session created')

        data = {
            "ProviderID":str(Station.objects.get(id=172220).providers.all().first().id),
            "StationID":"172220",
            "PointID":str(point.id),
            "PortID":str(point.ports.all().first().id),
            "VehicleID":"2",
            "kWh":True,
            "accharger":False,
            "kWhDelivered":30.5,
            "amount":'null',
            "connectionTime":"2020-08-09 10:41:10.00+00:00",
            "disconnectTime":"2020-08-09 12:41:10.00+00:00",
            "doneChargingTime":"2020-08-09 11:41:10.00+00:00",
            "payment":"Credit"
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Session created')

        # Test my bills
        url = reverse('mybills')
        response = self.client.get(url, data, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

        # Test my monthly bills
        url = reverse('mymonthlybills')
        response = self.client.get(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),1)

        # Test pay off 
        url = reverse('monthlypayoff')
        data = {"BillID": str(response.data[0]["id"])}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'Monthly bill is now paid')

        # Test refresh token
        url = reverse('token_refresh')
        data = {'refresh': token['refresh']}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test logout
        url = reverse('logout')
        data = token
        response = self.client.post(url,data, HTTP_AUTHORIZATION='JWT ' + response.data['access'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Test Login
        url = reverse('token_create')
        data = {'username' : 'KiriakosM', 'password' : 'eimaiokalyterosprwthypourgos'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data
        authorize = 'JWT ' + token['access']

        # Test deletion
        url = reverse('deleteme')
        response = self.client.delete(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(User.objects.filter(username='KiriakosM')), 0)


class AdminTest(APITestCase):
    def test_admin(self):
        
        SessionsTestCase().setUp()

        u = User.objects.create(username='admin', is_active=True, is_staff=True, is_superuser=True)
        u.set_password('petrol4ever')
        u.save()

        # Test superuser login
        url = reverse('token_create')
        data = {'username':'admin', 'password':'petrol4ever'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data
        authorize = 'JWT ' + token['access']


        # Test user creation
        url = reverse('usermod', kwargs={'username':'KiriakosM', 'password':'oibatsoieinaifiloimas'})
        response = self.client.post(url,HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'User successfully created')


        # Test password change
        url = reverse('usermod', kwargs={'username':'KiriakosM', 'password':'sike'})
        response = self.client.post(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],'Password successfully changed.')
       

        # Test inspectUser
        url = reverse('inspectuser', kwargs={'username':'KiriakosM'})
        response = self.client.get(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.data['username'],'KiriakosM')

        # Test reset sessions
        self.assertNotEqual(len(Session.objects.all()),0)
        url = reverse('resetsessions')
        response = self.client.post(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(len(Session.objects.all()),0)
        
        # Test healthcheck
        url = reverse('healthcheck')
        response = self.client.post(url, HTTP_AUTHORIZATION=authorize)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

        
