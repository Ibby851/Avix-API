
from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import *
# Create your views here.

class FarmRegistrationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = {'farm_name':request.data.get('farm_name'), 'farm_address':request.data.get('farm_address')}
        serializer = FarmRegistrationSerializer(data=data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(farmer=request.user)
            return Response({'status':'success'})
        return Response(serializer.errors)

class FarmListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        farms = Farm.objects.filter(farmer=request.user)
        serializer = FarmSerializer(farms, many=True)
        return Response(serializer.data)
    
class FarmDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        farm_obj = Farm.objects.get(id=request.data.get('farm_id'))
        farm_serializer = FarmSerializer(farm_obj)
        if Bird.objects.filter(farm=farm_obj).exists():
            bird = Bird.objects.get(farm=farm_obj) 
            bird_serializer = BirdSerializer(bird)
            return Response({'farm_info':farm_serializer.data, 'bird_info':bird_serializer.data})
        return Response({'farm_info':farm_serializer.data})

class FarmActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        activity_type = request.data.get('activity_type')
        farm_obj = Farm.objects.get(id=request.data.get('farm_id'))
        if activity_type == 'clear':
            if Bird.objects.filter(farm=farm_obj).exists():
                bird = Bird.objects.get(farm=farm_obj)
                bird.delete()
                return Response({'status':'success'},status=status.HTTP_200_OK)
            return Response({'status':'fail', 'message':'Farm is currenttly empty'})
        elif activity_type == 'start_raring':
            bird = Bird.objects.create(farm=farm_obj, bird_type=request.data.get('bird_type'), population=request.data.get('population'), age=request.data.get('age'))
            return Response({'status':'success'}, status=status.HTTP_201_CREATED)
        
        

