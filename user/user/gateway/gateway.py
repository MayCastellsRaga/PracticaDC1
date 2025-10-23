import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt


def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    # Publish to cloud MQTT
    cloud_client = mqtt.Client()
    cloud_client.connect("mosquitto_cloud", 1884, 60)
    cloud_client.publish(message.topic, message.payload)
    cloud_client.disconnect()
    print(type(message))


subscribe.callback(on_message_print, "#", hostname="mosquitto", port=1883)

