from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from auction_system import settings
import requests

from .serializers import CreateUserSerializer


CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET

IP_token = 'http://127.0.0.1:8000/o/token/'
IP_revoke_token ='http://127.0.0.1:8000/o/revoke_token/'


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    '''
    Registers user to the server. Input should be in the format:
    {"username": "xyz", "password": "1234abcd"}
    '''
    # Put the data from the request into the serializer
    serializer = CreateUserSerializer(data=request.data)
    # Validate the data
    if serializer.is_valid():
        # If it is valid, save the data (creates a user).
        serializer.save()
        # Then we get a token for the created user.
        # This could be done differentley
        r = requests.post(IP_token,
            data={
                'grant_type': 'password',
                'username': request.data['username'],
                'password': request.data['password'],
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
            },
        )
        return Response(r.json(), status=r.status_code)
    return Response(serializer.errors)



@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    '''
    Get token with username and password from server. Input should be in the format:
    {"username": "xyz", "password": "1234abcd"}
    '''
    r = requests.post(
    IP_token,
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json(), status=r.status_code)



@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    '''
    Refreshes the token from the server. Input should be in the format:
    {"refresh_token": "<token>"}
    '''
    r = requests.post(
    IP_token,
        data={
            'grant_type': 'refresh_token',
            'refresh_token': request.data['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    return Response(r.json(), status=r.status_code)


@api_view(['POST'])
@permission_classes([AllowAny])
def revoke_token(request):
    '''
    Method to revoke token.  Input should be in the format:
    {"token": "<token>"}
    '''
    r = requests.post(
        IP_revoke_token,
        data={
            'token': request.data['token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
        },
    )
    # If it goes well return success message (would be empty otherwise)
    if r.status_code == requests.codes.ok:
        return Response({'message': 'token revoked'}, r.status_code)
    # Return the error if it goes badly
    return Response(r.json(), r.status_code)
