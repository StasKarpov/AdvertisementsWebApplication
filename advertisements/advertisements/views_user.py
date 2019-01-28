from django.contrib.auth import authenticate, login, logout

from rest_framework import viewsets
from rest_framework import renderers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, mixins, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, permission_classes

from requests.exceptions import HTTPError

from django.contrib.auth.models import User
import re

USER_EXIST = 'User with given username already exists.'
TOKEN_ALREADY_GEN = 'User alredy logged in.'
UNAUTH_USER = 'Authentification failed.'

class UserCreationView(generics.CreateAPIView):
    '''
        User creation api view
    '''
    model = User
    permission_classes = [
        permissions.AllowAny # Everyone has access
    ]
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        if User.objects.filter(username=username).exists():
            return Response({'detail': USER_EXIST}, status=status.HTTP_400_BAD_REQUEST)

        if (username and email and password and
             re.match(r"[^@]+@[^@]+\.[^@]+", email)):
            user = User.objects.create_user(username,
                                            email,
                                            password)
            return Response(status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
        #todo check

class UserLoginView(APIView):
    '''
        Authenticates, logins and creates token!!!
    '''
    model = User
    permission_classes = [
        permissions.AllowAny # Everyone has access
    ]
    authentication_classes = (BasicAuthentication, )

    def post(self, request, format=None):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
                login(request, user)
                try:
                    token = Token.objects.create(user=user)
                    token.save()
                    return Response({'token': token.key}, status=status.HTTP_200_OK)
                except:
                    return Response({'detail': TOKEN_ALREADY_GEN}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': UNAUTH_USER},status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    '''
        User logout and deletes token
    '''
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication, )

    def post(self, request, format=None):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        logout(request)

        return Response(status=status.HTTP_200_OK)
