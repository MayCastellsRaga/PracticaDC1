from json import loads
from time import sleep
from kafka import KafkaConsumer
import logging
logging.basicConfig(level=logging.INFO)
my_consumer = KafkaConsumer(
    'test',
    bootstrap_servers=['localhost : 9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

print("starting")
for message in my_consumer:
    message = message.value
    print(f"{message} is being processed")
    sleep(1)
    print(f"{message} processed")
