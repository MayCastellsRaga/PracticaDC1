
from json import loads
from kafka import KafkaConsumer, KafkaProducer
import paho.mqtt.client as mqtt
import logging
import os
from json import dumps


logging.basicConfig(level=logging.INFO)
cloud_client= mqtt.Client()
cloud_client.connect("mosquitto_cloud",1884,60)
logging.info(f"please at least give me this")
print("please please")
producer = KafkaProducer(
    #bootstrap_servers=['mosquitto_cloud:1883'],
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
    )

consumer = KafkaConsumer(
    'clean', 
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='actuate',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
def check_sended(client, userdata, message):
    print(f"{client},{userdata},{message}")
for message in consumer:
    data = message.value
    dataValue = float(data.get("value",0))
    dataRoom = data.get("room","")
    dataUser =data.get("user","")
    dataTime =data.get("timestamp","")
    if dataValue >25:
        status= 0
        
    elif dataValue <=25:
        status= 1

    msg={

        "user": dataUser,
        "room": dataRoom,
        "timestamp": dataTime,
        "status": status,
    }
    cloud_client.publish(f"{dataUser}/kafka_heatpump",dumps(msg))
    cloud_client._on_publish= check_sended
