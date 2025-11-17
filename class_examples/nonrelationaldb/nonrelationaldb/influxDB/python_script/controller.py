import datetime
import time
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import random
bucket = "measurement"
org = "UDL"
url = "127.0.0.1:8086"
token = "secrettoken"

tag = "user1"
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


while True:
    value = random.uniform(20, 25)
    p = Point("indoor_metrics").tag("user", tag).field("temperature", value)
    write_api.write(bucket=bucket, record=p)
    print("%s %s" % ("temperature", value))
    time.sleep(1)
