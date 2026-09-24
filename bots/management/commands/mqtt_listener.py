import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from farms.models import *
import json
from datetime import datetime as dt
class Command(BaseCommand):
    help = 'RUNS THE MQTT LISTENER'

    def handle(self, *args, **options):
        def on_connect(client, userdata, flags, reason_code, properties):
            print('MQTT CONNECTION SUCCESSFUL')
            client.subscribe('environment/readings')
        def on_message(client, userdata, msg):
            reading = json.loads(msg.payload.decode())
            Reading.objects.create(bot_unique_id=reading.get('device_id'), temperature=reading.get('temperature_c'), ammonia=reading.get('ammonia_ppm'), humidity=reading.get('humidity'), recorded_at=dt.fromisoformat(reading.get('timestamp').replace('Z', "+00:00")), zone_index=reading.get('zone_index'))
            print(f"TOPIC: {msg.topic}")
            print(f"DATA RECEIVED: {json.loads(msg.payload.decode())}")

        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_connect = on_connect
        client.on_message = on_message
# DATA RECEIVED: {'device_id': 'AviX Robot 003', 'timestamp': '2026-09-22T17:43:19Z', 'zone_index': 8, 'ammonia_ppm': 15.5, 'temperature_c': 32.29999924, 'humidity': 67, 'nav_state': 'waypoint_pause'}
        client.connect('broker.hivemq.com', 1883)
        client.loop_forever()