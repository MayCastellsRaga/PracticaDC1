
from json import loads
from kafka import KafkaConsumer, KafkaProducer
import paho.mqtt.client as mqtt
import logging
import os
from json import dumps


logging.basicConfig(level=logging.INFO)
cloud_client= mqtt.Client()
cloud_client.connect("mosquitto_cloud",1883,60)
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
    group_id='group_clean_data',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

for message in consumer:
   
    logging.info(f"Received message from topic {message.topic}: {message.value}")
    data = message.value
    dataValue = float(data.get("value",0))
    dataRoom = data.get("room","")
    if dataValue >25:
        status= False
        cloud_client.publish(f"{dataRoom}/heatpump",status)
        logging.info(f"sended order to controler:  {status}")
    elif dataValue <=25:
        status= True
        cloud_client.publishf(f"{dataRoom}/heatpump",status)
        logging.info(f"Sent cleaned data to 'clean' topic: {status}")