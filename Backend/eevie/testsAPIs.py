from rest_framework.test import APIRequestFactory, APITestCase, force_authenticate
from django.urls import reverse
from eevie.models import *
from eevie.views import *
from eevie.tests import ReferenceTest

class UserInterferenceTest(APITestCase):
    def test_signup(self):

        ReferenceTest().setUp()
        
        # Test Signup
        url = reverse('signup')
        data = {'username' : 'KiriakosM', 'password' : 'eimaiokalyterosprwthypourgos', 'car_id' : '5663b87a-d940-4bab-9846-d74c8c0ae260'}
        response = self.client.post(url,data)
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

        # Test mycars
        url = reverse('mycars')
        response = self.client.get(url, HTTP_AUTHORIZATION=authorize)
        print(json.dumps(response.data, indent=2))

        
