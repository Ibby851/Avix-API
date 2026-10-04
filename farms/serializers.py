from rest_framework import serializers
from .models import Farm, Bird, Bot, Reading, House, Worker



class FarmRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['name', 'address', 'farmer']
        read_only_fields = ['farmer']
    def validate(self, attrs):
        if Farm.objects.filter(farmer=self.context.get('request').user,name=attrs.get('name'), address=attrs.get('address')).exists():
            raise serializers.ValidationError(f"You already have a farm with the name '{attrs.get('name')}' and address '{attrs.get('address')}'")
        return attrs
    def create(self, validated_data):
        farm = Farm.objects.create(farmer=validated_data.get('farmer'), address=validated_data.get('address'), name=validated_data.get('name'))
        return farm


class FarmSerializer(serializers.ModelSerializer):
    houses_count = serializers.SerializerMethodField()
    workers_count = serializers.SerializerMethodField()
    class Meta:
        model = Farm
        fields = ['id','name', 'address','houses_count','workers_count','created_at']
        read_only_fields = fields

    def get_houses_count(self, obj) -> int:
        return obj.houses.count()

    def get_workers_count(self, obj) -> int:
        return Worker.objects.filter(farm_id=obj.id).count()


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


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['full_name', 'phone_number','role', 'id', 'shift']
        read_only_fields = ['id']

