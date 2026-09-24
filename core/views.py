

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer
from .serializers import *
# Create your views here.

class LogoutView(APIView):
    @extend_schema(
        summary='Log out the current user',
        request=None,
        responses=inline_serializer(
            name='LogoutResponse',
            fields={'detail': serializers.CharField()},
        ),
    )
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail":"Successfully logged out"})


class RegistrationView(APIView):
    @extend_schema(
        summary='Register a user',
        request=UserRegistrationSerializer,
        responses=inline_serializer(
            name='RegistrationResponse',
            fields={'status': serializers.CharField()},
        ),
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":'success'})
        else:
            return Response(serializer.errors)

class AccountInfoUpdate(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Update the current user account',
        request=UserRegistrationSerializer,
        responses=inline_serializer(
            name='AccountUpdateResponse',
            fields={'status': serializers.CharField()},
        ),
    )
    def post(self,request):
        serializer = UserRegistrationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success"})
        return Response(serializer.errors)

