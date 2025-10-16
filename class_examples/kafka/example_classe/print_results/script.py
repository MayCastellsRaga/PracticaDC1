from json import dumps, loads
from kafka import KafkaProducer
from kafka import KafkaConsumer
import logging
logging.basicConfig(level=logging.INFO)
my_consumer = KafkaConsumer(
    'comfort_temperature',
    bootstrap_servers=['localhost : 9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

for message in my_consumer:
    print(f"the comfort difference is : {message.value['comfort']}")
