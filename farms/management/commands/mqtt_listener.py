import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from farms.models import *
import json
from datetime import datetime as dt
from farms.mqtt_services import HiveMQClient
from django.conf import settings
class Command(BaseCommand):
    help = 'RUNS THE MQTT LISTENER'

    def handle(self, *args, **options):
        mqtt_obj = HiveMQClient(settings.MQTT_HOST_NAME, settings.MQTT_PORT, 'AviX-Service-Listener')
        mqtt_obj.run('listener')
