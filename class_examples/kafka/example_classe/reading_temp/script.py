from time import sleep
from json import dumps
from kafka import KafkaProducer
import random as r
my_producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
    )
while True:
    my_data = {'tempreature': r.randint(10,30)}
    print(my_data)
    my_producer.send('raw_temperature', value=my_data)
    sleep(2)
