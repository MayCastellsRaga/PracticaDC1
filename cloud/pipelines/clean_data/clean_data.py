
from json import loads
from kafka import KafkaConsumer, KafkaProducer
import logging
from influxdb_client import InfluxDBClient, Point
import os
from json import dumps


logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda x: dumps(x).encode('utf-8')
    )

consumer = KafkaConsumer(
    'raw', 
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='group_clean_data',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

for message in consumer:
    logging.info(f"Received message from topic {message.topic}: {message.value}")
    data = message.value
    if data.get("value") == 100.0:
        logging.warning(f"Invalid data detected: {data}")
        continue  # Skip invalid data
    producer.send('clean', value=data)
    logging.info(f"Sent cleaned data to 'clean' topic: {data}")