

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer
from .serializers import *
# Create your views here.

class LoginView(ObtainAuthToken):
    @extend_schema(
        summary='Log in with username and password',
        auth=[],
        request=inline_serializer(
            name='LoginRequest',
            fields={
                'username': serializers.CharField(),
                'password': serializers.CharField(),
            },
        ),
        responses=inline_serializer(
            name='LoginResponse',
            fields={'token': serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                'Login request',
                value={'username': 'alaba_user', 'password': 'ExamplePass123!'},
                request_only=True,
            ),
            OpenApiExample(
                'Login response',
                value={'token': '0123456789abcdef0123456789abcdef01234567'},
                response_only=True,
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    @extend_schema(
        summary='Log out the current user',
        request=None,
        responses=inline_serializer(
            name='LogoutResponse',
            fields={'status': serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                'Logout response',
                value={'status': 'success'},
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"status":"success"})


class RegistrationView(APIView):
    @extend_schema(
        summary='Register a user',
        request=UserRegistrationSerializer,
        responses=inline_serializer(
            name='RegistrationResponse',
            fields={'status': serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                'Registration request',
                value={
                    'username': 'alaba_user',
                    'first_name': 'Alaba',
                    'last_name': 'Adebayo',
                    'phone_number': '+2348012345678',
                    'email': 'alaba@example.com',
                    'password': 'ExamplePass123!',
                    'password_confirmation': 'ExamplePass123!',
                },
                request_only=True,
            ),
            OpenApiExample(
                'Registration response',
                value={'status': 'success'},
                response_only=True,
            ),
        ],
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":'success'})
        else:
            return Response(serializer.errors)

class AccountUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Update the current user account',
        request=UserRegistrationSerializer,
        responses=inline_serializer(
            name='AccountUpdateResponse',
            fields={'status': serializers.CharField()},
        ),
        examples=[
            OpenApiExample(
                'Account update request',
                value={
                    'first_name': 'Alaba',
                    'last_name': 'Adebayo',
                    'phone_number': '+2348012345678',
                    'email': 'alaba@example.com',
                },
                request_only=True,
            ),
            OpenApiExample(
                'Account update response',
                value={'status': 'success'},
                response_only=True,
            ),
        ],
    )

    def patch(self,request):
        serializer = UserRegistrationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success"})
        return Response(serializer.errors)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='View the current user profile',
        responses=ProfileSerializer,
        examples=[
            OpenApiExample(
                'Profile response',
                value={
                    'first_name': 'Alaba',
                    'last_name': 'Adebayo',
                    'email': 'alaba@example.com',
                    'username': 'alaba_user',
                    'phone_number': '+2348012345678',
                    'farms_count': 2,
                    'bots_count': 1,
                },
                response_only=True,
            ),
        ],
    )
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)


