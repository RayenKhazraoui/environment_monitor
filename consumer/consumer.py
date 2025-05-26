import os, json, psycopg2
from confluent_kafka import Consumer

consumer = Consumer({
    'bootstrap.servers': os.environ['KAFKA_BOOTSTRAP_SERVERS'],
    'group.id': 'sensor-consumer',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['indoor.env_data'])

conn = psycopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD']
)
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_measurements (
    id SERIAL PRIMARY KEY,
    device_id TEXT,
    timestamp TIMESTAMP,
    temperature REAL,
    humidity REAL,
    pressure REAL
)
""")
conn.commit()

while True:
    msg = consumer.poll(1.0)
    if msg is None or msg.error(): continue
    data = json.loads(msg.value())
    cur.execute("""
        INSERT INTO sensor_measurements (device_id, timestamp, temperature, humidity, pressure)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        data["device_id"],
        data["timestamp"],
        data["temperature"],
        data["humidity"],
        data["pressure"]
    ))
    conn.commit()

    print(f"Inserted: {data}")
