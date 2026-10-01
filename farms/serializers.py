from rest_framework import serializers
from .models import Farm, Bird, Bot, Reading, House



class FarmRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['name', 'address', 'farmer']
        read_only_fields = ['farmer']
    def validate(self, attrs):
        if Farm.objects.filter(farmer=self.context.get('request').user, farm_name=attrs.get('name'), farm_address=attrs.get('address')).exists():
            raise serializers.ValidationError('You already register this farm')
        return attrs
    def create(self, validated_data):
        farm = Farm.objects.create(farmer=validated_data.get('farmer'), farm_address=validated_data.get('address'), farm_name=validated_data.get('name'))
        return farm


class FarmSerializer(serializers.ModelSerializer):
    houses_count = serializers.SerializerMethodField()
    class Meta:
        model = Farm
        fields = ['id','name', 'address','houses_count','created_at']
        read_only_fields = fields

    def get_houses_count(self, obj) -> int:
        return obj.houses.count()

class BirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bird
        fields = ['bird_type', 'age', 'population', 'raring_starts_at']

class BotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bot
        fields = ['name','unique_id']

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ['temperature', 'humidity', 'ammonia', 'recorded_at', 'zone_index']


class HouseSerializer(serializers.ModelSerializer):
    devices_count = serializers.SerializerMethodField()
    class Meta:
        model = House
        fields = ['id', 'name', 'devices_count','tracks', 'created_at']

    def get_devices_count(self, obj) -> int:
        return obj.bots.count()

class HouseSerializer(serializers.ModelSerializer):
    devices_count = serializers.SerializerMethodField()
    bots = BotSerializer(many=True)
    class Meta:
        model = House
        fields = ['id', 'name', 'devices_count','tracks','zones','bots','created_at']

    def get_devices_count(self, obj) -> int:
        return obj.bots.count()

