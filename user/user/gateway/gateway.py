
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import json
import os

cloud_client = mqtt.Client()
cloud_client.connect("mosquitto_cloud", 1884, 60)


project_name = os.environ.get("PROJECT_NAME", "default")
print("Project name:", project_name)

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    # Publish to cloud MQTT
    try:
        payload = json.loads(message.payload.decode("utf-8"))
    except Exception as e:
        print(f"Error decoding payload: {e}")
        return
    data = {
        "user": project_name,
        "room": message.topic.replace("/temperature", ""),
        "timestamp": payload.get("timestamp", ""),
        "value": payload.get("value", "")
    }
    cloud_client.publish("main", json.dumps(data))
    print("Published to cloud:", data)
    #cloud_client.disconnect()



subscribe.callback(on_message_print, "+/temperature", hostname="mosquitto", port=1883)

