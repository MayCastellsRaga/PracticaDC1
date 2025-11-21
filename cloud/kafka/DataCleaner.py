#from json import dumps, loads
#from time import sleep
#from kafka import KafkaProducer
#from kafka import KafkaConsumer
#import logging
#
#logging.basicConfig(level=logging.INFO)
#
#my_consumer = KafkaConsumer(
#    'raw_data',
#    bootstrap_servers=['localhost: 1884'],
#    auto_offset_reset='latest',
#    enable_auto_commit=True,
#    group_id='raw_group',
#    value_deserializer=lambda x: loads(x.decode('utf-8'))
#)
#my_producer = KafkaProducer(
#    'clean_data',
#    bootstrap_servers=['localhost:1884'],
#    enable_auto_commit=True,
#    group_id='clean_group',
#    value_deserializer=lambda x: loads(x.decode('utf-8'))
#)
#
#print("starting")
#for message in my_consumer:
#
#    message = message.value
#    if message != 100:
#        my_producer.send('clean_data',message)
#        print(f"{message} processed")
