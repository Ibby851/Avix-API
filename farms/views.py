
from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from drf_spectacular.utils import OpenApiExample, extend_schema, inline_serializer
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
        examples=[
            OpenApiExample(
                'Farm list response',
                value={
                    'id': 1,
                    'name': 'Green Valley Farm',
                    'address': '12 Farm Road, Ibadan',
                    'devices_count': 1,
                    'created_at': '2026-10-01T09:30:00Z',
                },
                response_only=True,
            ),
        ],
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
    def get(self, request, id):
        farm_obj = Farm.objects.get(id=id)
        farm_serializer = FarmSerializer(farm_obj)
        house_serializer = HouseSerializer(farm_obj.houses.all(), many=True)
        return Response({'farm_detail':farm_serializer.data, 'houses_details':house_serializer.data})



class HouseDetail(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, reqeuest, id):
        house_obj = House.objects.get(id=id)
        house_serializer = HouseSerializer(house_obj)
        return Response(house_serializer.data)

class RegisterBot(APIView):
    def post(self, request):
        if Bot.objects.filter(unique_id=request.data.get('unique_id')).exists():
            return Response({'status':'fail','message':'Bot has already been registered'})
        house = House.objects.get(id=request.data.get('id'))
        bot = Bot.objects.create(house=house, unique_id=request.data.get('unique_id'),name=request.data.get('name'))
        bot_serializer = BotSerializer(bot)
        return Response({'status':'success', 'bot_data':bot_serializer.data})

class RegisterHouse(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        name = request.data.get('name')
        farm = Farm.objects.get(id=data.get('id'))
        if House.objects.filter(farm=farm,name=name).exists():
            return Response({'status':'fail', 'messagge':'This house already exist on your farm'})
        house = House.objects.create(name=data.get('name'), farm=farm, zones=data.get('zones'), tracks=data.get('tracks'))
        house_serializer = HouseSerializer(house)
        return Response({"status":'success', 'house_data':house_serializer.data})

        

            
        
        

