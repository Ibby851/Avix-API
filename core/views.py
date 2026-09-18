

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
# Create your views here.

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response({"detail":"Successfully logged out"})


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":'success'})
        else:
            return Response(serializer.errors)

class AccountInfoUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer = UserRegistrationSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":"success"})
        return Response(serializer.errors)

