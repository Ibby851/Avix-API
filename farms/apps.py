from django.apps import AppConfig


class FarmsConfig(AppConfig):
    name = 'farms'
    # def ready(self):
    #     from .mqtt_services import mqtt_obj
    #     from django.conf import settings
    #     self.publisher = mqtt_obj
    #     self.publisher.run('publisher')

