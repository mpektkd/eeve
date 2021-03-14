import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth.models import User


class SafeJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_heaader = request.headers.get('X-OBSERVATORY-AUTH')
        if authorization_heaader == 'null':
            return None
        if not authorization_heaader:
            return None
        try:
            access_token = authorization_heaader
            try:
                payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.DecodeError:
                raise exceptions.AuthenticationFailed('GTXS')
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')

        user = User.objects.filter(username=payload['username']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return (user, None)