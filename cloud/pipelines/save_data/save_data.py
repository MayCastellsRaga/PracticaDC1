
from json import loads
from kafka import KafkaConsumer
import logging
from influxdb_client import InfluxDBClient, Point
import os

logging.basicConfig(level=logging.INFO)

# InfluxDB config from environment
INFLUXDB_URL = os.environ.get('INFLUXDB_URL', 'http://influxdb:8086')
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', 'secrettoken')
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG', 'UDL')
INFLUXDB_BUCKET_RAW = os.environ.get('INFLUXDB_BUCKET', 'raw_data')
INFLUXDB_BUCKET_CLEAN = os.environ.get('INFLUXDB_BUCKET_CLEAN', 'clean_data')

# Set up InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api()

consumer = KafkaConsumer(
    'raw', 'clean',
    bootstrap_servers=['kafka:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='group_save_data',
    value_deserializer=lambda x: loads(x.decode('utf-8'))
)

for message in consumer:
    logging.info(f"Received message from topic {message.topic}: {message.value}")
    data = message.value
    # Choose bucket based on topic
    if message.topic == 'raw':
        bucket = INFLUXDB_BUCKET_RAW
        measurement = "raw_temperature"
    else:
        bucket = INFLUXDB_BUCKET_CLEAN
        measurement = "clean_temperature"
    point = Point(measurement) \
        .tag("user", data.get("user", "")) \
        .tag("room", data.get("room", "")) \
        .field("value", float(data.get("value", 0))) \
        .time(data.get("timestamp"))
    write_api.write(bucket=bucket, org=INFLUXDB_ORG, record=point)