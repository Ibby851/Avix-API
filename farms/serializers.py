from rest_framework import serializers
from .models import Farm, Bird


class FarmRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['farm_name', 'farm_address', 'farmer']
        read_only_fields = ['farmer']
    def validate(self, attrs):
        if Farm.objects.filter(farmer=self.context.get('request').user, farm_name=attrs.get('farm_name'), farm_address=attrs.get('farm_address')).exists():
            raise serializers.ValidationError('You already register this farm')
        return attrs
    def create(self, validated_data):
        farm = Farm.objects.create(farmer=validated_data.get('farmer'), farm_address=validated_data.get('farm_address'), farm_name=validated_data.get('farm_name'))
        request = self.context.get('request')
        bird = Bird.objects.create(farm=farm, bird_type=request.data.get('bird_type'), age=request.data.get('age'), population=request.data.get('population'))
        return farm


class FarmSerializer(serializers.ModelSerializer):
    bots_count = serializers.SerializerMethodField()
    class Meta:
        model = Farm
        fields = ['id','farm_name', 'farm_address', 'bots_count','created_at']
        read_only_fields = fields

    def get_bots_count(self, obj):
        return obj.bots.count()

class BirdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bird
        fields = ['bird_type', 'age', 'population', 'raring_starts_at']
        

