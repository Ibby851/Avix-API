import paho.mqtt.client as mqtt_client
from django.conf import settings
from .models import Reading, Bot, Farm
import json
from datetime import datetime as dt

class HiveMQClient:
    def __init__(self, host, port, client_id):
        self.host = host
        self.port = port
        self.client_id = client_id
        self.client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, self.client_id,protocol=mqtt_client.MQTTv311)


    def setup(self):
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        
    def on_connect(self, client, userdata, flags, reason_code, properties):
        self.client.subscribe('avix/devices/readings',qos=2)
        self.client.subscribe('avix/devices/railmap-data', qos=2)

    def on_message(self, client, userdata, message):
        data = json.loads(message.payload.decode('utf-8'))
        
        if message.topic == 'avix/devices/readings':
            bot_mac_address = data[0]
            if Bot.objects.filter(mac=bot_mac_address).exists():
                bot = Bot.objects.get(mac=bot_mac_address)
                time_stamp = dt.fromisoformat(data[1].replace('Z', "+00:00"))
                zone_index = data[2]
                ammonia = data[3]
                temperature = data[4]
                humidity = data[5]
                Reading.objects.create(bot=bot,zone_index=zone_index, ammonia=ammonia, temperature=temperature, humidity=humidity, recorded_at=time_stamp)
                print(f"Reading saved for the bot with mac address {bot_mac_address}. Data is {data}")
            else:
                ...
        else:
            bot_mac_address = data[0]
            if Bot.objects.filter(mac=bot_mac_address).exists():
                bot_obj = Bot.objects.get(mac=bot_mac_address)
                bot_obj.zone_count = data[-1]
                bot_obj.save()
                print(f"Railmap data updated for the bot with mac address {bot_mac_address}. Data is {data}")
            else:
                pass
        

    def publish(self, mac_address,payload):
        self.client.publish('avix/devices/command/',json.dumps(payload), qos=2)
        print(f'The command {payload} sent to bot of address {mac_address}')



    def run(self, run_mode):
        self.setup()
        self.client.connect(self.host, self.port)
        if run_mode == 'listener':
            self.client.loop_forever(retry_first_connection=True)
        else:
            self.client.loop_start()


mqtt_obj = HiveMQClient(settings.MQTT_HOST_NAME, settings.MQTT_PORT, 'AviX-Service')




