import os, json, psycopg2
from confluent_kafka import Consumer

# Kafka consumer configuration (same as your existing script)
consumer = Consumer({
    'bootstrap.servers': os.environ['KAFKA_BOOTSTRAP_SERVERS'],
    'group.id': 'sensor-consumer',
    'auto.offset.reset': 'earliest'
})

# Subscribe to the new CO2 topic
consumer.subscribe(['indoor.co2'])

# Postgres connection (same env-vars/config as before)
conn = psycopg2.connect(
    host=os.environ['POSTGRES_HOST'],
    port=os.environ['POSTGRES_PORT'],
    dbname=os.environ['POSTGRES_DB'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD']
)
cur = conn.cursor()

# Create a new table for the CO2 readings
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_co2_measurements (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP,
    location TEXT,
    co2_ppm REAL
)
""")
conn.commit()

# Consume and insert loop
while True:
    msg = consumer.poll(1.0)
    if msg is None or msg.error():
        continue

    data = json.loads(msg.value())
    cur.execute("""
        INSERT INTO sensor_co2_measurements (timestamp, location, co2_ppm)
        VALUES (%s, %s, %s)
    """, (
        data["timestamp"],
        data["location"],
        data["co2_ppm"]
    ))
    conn.commit()

    print(f"Inserted CO2 reading: {data}")
