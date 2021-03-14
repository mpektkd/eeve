from eevie.serializers import UserSerializer

def jwt_response_handler(token, user=None, request=None):
    print(UserSerializer(user,context={'request': request}).data)
    return {
        'token': token,
        'user': UserSerializer(user,context={'request': request}).data
    }