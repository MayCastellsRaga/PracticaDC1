from json import dumps, loads
from kafka import KafkaProducer
from kafka import KafkaConsumer
import random as r

import logging
logging.basicConfig(level=logging.INFO)
my_consumer = KafkaConsumer(
    'clean_temperature',
    bootstrap_servers=['localhost : 9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)
my_producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
    )
for message in my_consumer:
    value_dict = message.value
    if 20 > value_dict['temperature']:
        comfort = 20 - value_dict['temperature']
        my_producer.send('comfort_temperature', value={"comfort": comfort})
    elif 25 < value_dict['temperature']:
        comfort = value_dict['temperature'] - 25
        my_producer.send('comfort_temperature', value={"comfort": comfort})
    else:
        comfort = 0
        my_producer.send('comfort_temperature', value={"comfort": comfort})

