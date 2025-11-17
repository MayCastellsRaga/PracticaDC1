import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    cloud_client = mqtt.Client()
    cloud_client.connect("localhost", 1884, 60)
    cloud_client.publish("raw_data", message.payload)
    cloud_client.disconnect()
subscribe.callback(on_message_print, "#", hostname="mosquitto_cloud")

