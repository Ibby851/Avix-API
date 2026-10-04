from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
User = get_user_model()

class Farm(models.Model):
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def bots_count(self):
        return self.bots.count()


class Bot(models.Model):
    house = models.ForeignKey('House',related_name='bots', on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=25, default='AviX Bot')
    installed_at = models.DateTimeField(auto_now_add=True)


class Bird(models.Model):
    farm = models.OneToOneField(Farm, on_delete=models.CASCADE)
    bird_type = models.CharField(max_length=50)
    age = models.IntegerField()
    population = models.IntegerField()
    raring_starts_at = models.DateTimeField(auto_now_add=True)

class Reading(models.Model):
    bot = models.ForeignKey(Bot,on_delete=models.SET_NULL, related_name='readings', null=True)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='farm_readings')
    temperature = models.FloatField()
    humidity = models.FloatField()
    ammonia = models.FloatField()
    recorded_at = models.DateTimeField(auto_now_add=True)
    zone_index = models.IntegerField()

class House(models.Model):
    farm = models.ForeignKey(Farm, related_name='houses', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    tracks = models.PositiveIntegerField()
    zones = models.JSONField(default=dict)
    created_at = models.DateField(auto_now_add=True)


class Worker(models.Model):
    SHIFT_CHOICES = [
        ('day', 'Day'),
        ('night', 'Night'),
        ('any', "Any")
    ]
    farm = models.ForeignKey(Farm, related_name='workers', on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True)
    role = models.CharField(max_length=100)
    added_at = models.DateField(auto_now_add=True)
    shift = models.CharField(max_length=100, choices=SHIFT_CHOICES, default='any')


    


    

