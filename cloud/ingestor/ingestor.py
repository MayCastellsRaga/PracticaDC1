from json import dumps
import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer
import json


producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
    )

def on_message_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    producer.send('raw', value=json.loads(message.payload.decode("utf-8")))
    
subscribe.callback(on_message_print, "main", hostname="mosquitto_cloud")

# \# to subscribe to all topics