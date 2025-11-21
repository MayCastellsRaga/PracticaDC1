import faust
from influxdb_client import InfluxDBClient, Point
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.INFO)

# InfluxDB config
INFLUXDB_URL = os.environ.get('INFLUXDB_URL', 'http://influxdb:8086')
INFLUXDB_TOKEN = os.environ.get('INFLUXDB_TOKEN', 'secrettoken')
INFLUXDB_ORG = os.environ.get('INFLUXDB_ORG', 'UDL')
INFLUXDB_BUCKET = os.environ.get('INFLUXDB_BUCKET_AGGREGATE', 'aggregate_data')

# Set up InfluxDB client and create bucket if not exists
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api()


app = faust.App(
    'aggregate',
    broker='kafka://kafka:9092',
    value_serializer='json',
)

# Reading model
class Reading(faust.Record, serializer='json'):
    user: str
    room: str
    value: float
    timestamp: str

# Topic
clean_topic = app.topic('clean', value_type=Reading)

user_sum_table = app.Table('user_sum', default=float)
user_count_table = app.Table('user_count', default=int)

last_aggregated = {}

@app.agent(clean_topic)
async def aggregate(stream):
    async for reading in stream.group_by(Reading.user):
        logging.info(f"Received reading from user {reading.user}: {reading.value}°C")
        
        # Acumula suma i count
        user_sum_table[reading.user] += reading.value
        user_count_table[reading.user] += 1

@app.timer(5.0, on_leader=True)
async def save_aggregates():
    # Snapshot de les taules en aquest moment
    current_sums = dict(user_sum_table.items())
    current_counts = dict(user_count_table.items())
    
    for user, total in current_sums.items():
        count = current_counts.get(user, 0)
        
        # Obtenir l'última agregació guardada
        last_total, last_count = last_aggregated.get(user, (0.0, 0))
        
        # Calcular diferència (només les noves lectures dels últims 5 segons)
        delta_total = total - last_total
        delta_count = count - last_count
        
        if delta_count > 0:
            avg_temp = delta_total / delta_count
            timestamp = datetime.now().isoformat()
            
            logging.info(f"Aggregate for user {user}: {avg_temp:.2f}°C (from {delta_count} readings)")
            
            point = Point("user_aggregate") \
                .tag("user", user) \
                .field("mean_temperature", avg_temp) \
                .field("reading_count", delta_count) \
                .time(timestamp)
            
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            
            # Actualitzar el tracking
            last_aggregated[user] = (total, count)

if __name__ == '__main__':
    app.main()