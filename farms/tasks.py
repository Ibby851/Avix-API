

def send_command(mac_address, command_payload):
    from .mqtt_services import mqtt_obj
    mqtt_obj.publish(mac_address=mac_address, payload=command_payload)

