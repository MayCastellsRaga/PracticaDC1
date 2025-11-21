
import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
import json
import os
import time
import threading
mqtt_host = os.getenv("MQTT_HOST")


project_name = os.environ.get("PROJECT_NAME", "default")
print("Project name:", project_name)


def on_message_print(client, userdata, message):
    cloud_client = mqtt.Client()
    cloud_client.connect("mosquitto_cloud", 1884, 60)
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
def on_message_sensor(client,userdata,message):
    user_client = mqtt.Client()
    user_client.connect(mqtt_host, 1883, 60)
    print("%s %s" % (message.topic, message.payload))
    try:
        payload = json.loads(message.payload.decode("utf-8"))
    except Exception as e:
        print(f"error decoding payload: {e}")
        return
    print("Payload value:",payload)
    print("message value:",message.payload)
    data = {
        "user":project_name,
        "room": payload.get("room",""),
        "timpestamp": payload.get("timestamp",""),
        "value": payload.get("value","")
    }
    user_client.publish("user2/heatpump",json.dumps(data))
    print("Published to controler:", data)


#///// Will handle messages from controler to the gateway and send it to the cloud /////

mosquito_client=mqtt.Client()
mosquito_client.connect(mqtt_host,1883,60)
mosquito_client.loop_start()
mosquito_client.subscribe("+/temperature")
mosquito_client.on_message = on_message_print
#////////////////////////////////////////////

#///// Will handle messages from kafka to the gateway and then send them to the controler/////

kafka_client =mqtt.Client()
kafka_client.connect("mosquitto_cloud",1884,60)
kafka_client.subscribe(f"{project_name}/kafka_heatpump",)
kafka_client.on_message = on_message_sensor
kafka_client.loop_start()

#////////////////////////////////////////////


while True:
    time.sleep(1)