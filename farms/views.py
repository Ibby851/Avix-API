
from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, inline_serializer
from .serializers import *
from .models import *
# Create your views here.

class FarmRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Register a farm',
        request=inline_serializer(
            name='FarmRegistrationRequest',
            fields={
                'farm_name': serializers.CharField(),
                'farm_address': serializers.CharField(),
                'bird_type': serializers.CharField(required=False),
                'age': serializers.IntegerField(required=False),
                'population': serializers.IntegerField(required=False),
            },
        ),
        responses=inline_serializer(
            name='FarmRegistrationResponse',
            fields={'status': serializers.CharField()},
        ),
    )
    def post(self, request):
        data = {'farm_name':request.data.get('farm_name'), 'farm_address':request.data.get('farm_address')}
        serializer = FarmRegistrationSerializer(data=data, context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save(farmer=request.user)
            return Response({'status':'success'})
        return Response(serializer.errors)

class FarmListView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='List the current user farms',
        responses=FarmSerializer(many=True),
    )
    def get(self, request):
        farms = Farm.objects.filter(farmer=request.user)
        serializer = FarmSerializer(farms, many=True)
        return Response(serializer.data)
    
class FarmDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get farm details',
        request=inline_serializer(
            name='FarmDetailRequest',
            fields={'farm_id': serializers.IntegerField()},
        ),
        responses=inline_serializer(
            name='FarmDetailResponse',
            fields={
                'farm_info': FarmSerializer(),
                'bird_info': BirdSerializer(required=False),
            },
        ),
    )
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

    @extend_schema(
        summary='Perform an activity on a farm',
        request=inline_serializer(
            name='FarmActivityRequest',
            fields={
                'activity_type': serializers.ChoiceField(
                    choices=['clear', 'start_raring', 'register_bot'],
                ),
                'farm_id': serializers.IntegerField(),
                'bird_type': serializers.CharField(required=False),
                'population': serializers.IntegerField(required=False),
                'age': serializers.IntegerField(required=False),
                'unique_id': serializers.CharField(required=False),
                'name': serializers.CharField(required=False),
            },
        ),
        responses=inline_serializer(
            name='FarmActivityResponse',
            fields={
                'status': serializers.CharField(),
                'message': serializers.CharField(required=False),
                'data': BotSerializer(required=False),
            },
        ),
    )
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
        elif activity_type == "register_bot":
            if Bot.objects.filter(unique_id=request.data.get('unique_id')).exists():
                return Response({'status':'fail'})
            else:
                data = request.data
                bot = Bot.objects.create(farm=Farm.objects.get(id=data.get('farm_id')), unique_id=data.get('unique_id'), name=data.get('name'))
                serializer = BotSerializer(bot)
                return Response({'status':'success', 'data':serializer.data})
            
        
        

