from rest_framework import serializers
from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'password', 'email', 'username', 'password_confirmation', 'phone_number']
        read_only_fields = ['is_active', 'is_staff', 'is_superuser']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError({'password_confirmation':'Password do not match.'})
        return attrs

    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(f"User with the username '{value}' already exist.")
        elif len(value) < 5:
            raise serializers.ValidationError(f"Username can not have less than five characters")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"User with the email '{value}' already exist.")
        return value

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError(f"The phone number '{value}' already exist.")
        return value

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
