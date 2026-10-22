from rest_framework import serializers
from .models import Farm, Bird, Bot, Reading, House, Worker



class FarmSerializer(serializers.ModelSerializer):
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
    farm_id = serializers.IntegerField(source='id', required=False, read_only=True)
    class Meta:
        model = Farm
        fields = ['farm_id','name', 'address','houses_count','workers_count','created_at']
        read_only_fields = ['farm_id', 'created_at']

    def validate(self, attrs):
        if Farm.objects.filter(farmer=self.context.get('request').user,name=attrs.get('name'), address=attrs.get('address')).exists():
            raise serializers.ValidationError(f"You already have a farm with the name '{attrs.get('name')}' and address '{attrs.get('address')}'")
        return attrs
    def create(self, validated_data):
        farm = Farm.objects.create(farmer=validated_data.get('farmer'), address=validated_data.get('address'), name=validated_data.get('name'))
        return farm

    def get_houses_count(self, obj) -> int:
        return obj.houses.count()

    def get_workers_count(self, obj) -> int:
        return Worker.objects.filter(farm_id=obj.id).count()


class BirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bird
        fields = ['bird_type', 'age', 'population', 'raring_starts_at']

class BotSerializer(serializers.ModelSerializer):
    device_id = serializers.IntegerField(source="id", required=False, read_only=True)
    house_id = serializers.PrimaryKeyRelatedField(source='house', queryset=House.objects.all())
    class Meta:
        model = Bot
        fields = ['device_id','mac', 'track_label', 'installed_at', 'house_id', 'zone_count']
    def create(self, validated_data):
        return Bot.objects.create(**validated_data)
        

class ReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reading
        fields = ['temperature', 'humidity', 'ammonia', 'zone_index','recorded_at']



class HouseSerializer(serializers.ModelSerializer):
    devices_count = serializers.SerializerMethodField()
    house_id = serializers.IntegerField(source='id', read_only=True, required=False)
    bots = BotSerializer(many=True, read_only=True)
    class Meta:
        model = House
        fields = ['house_id', 'name', 'devices_count','length_m','width_m','height_m', 'created_at', 'bots']
        read_only_fields = ['created_at', 'house_id']

    def get_devices_count(self, obj) -> int:
        return obj.bots.count()

    def create(self, validated_data):
        farm = Farm.objects.get(id=self.context.get('farm_id'))
        return House.objects.create(**validated_data, farm=farm)

    


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['full_name', 'phone_number','role', 'id', 'shift']
        read_only_fields = ['id']

