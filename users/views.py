from django.contrib import auth
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import RegisterSerializer, ResetPasswordSerializer, LoginSerializer


class RegisterUserAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid(raise_exception=True):
            registerdata = serializer.save()
            data['response'] = 'Successfully registered'
            data['username'] = registerdata.username
            data['email'] = registerdata.email
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            auth.login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response('Invalid username and password try again')


class LogoutAPIView(APIView):

    def get(self, request):
        request.user.auth_token.delete()
        auth.logout(request)
        return Response('Successfully logged out')


class ResetPasswordAPIView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        alldatas = {}
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            alldatas['data'] = 'Successfully reset'
            return Response(alldatas)
        return Response('Failed retry after some time')

