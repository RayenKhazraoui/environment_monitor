import time
import json
from datetime import datetime
from confluent_kafka import Producer
import random

import board
import busio
from adafruit_bme280 import basic as adafruit_bme280

# Kafka setup (vervang IP indien nodig)
producer = Producer({
    'bootstrap.servers': '192.168.0.113:29092'
})

# Initialize I2C + sensor
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, address=0x76)

i=0

while i<50:
    event = {
        "device_id": "pi_bme280",
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(bme280.temperature, 2),
        "humidity": round(bme280.humidity, 1),
        "pressure": round(bme280.pressure, 1),
        "co2_ppm": random.randint(400, 1500)
    }

    producer.produce("indoor.env_data", json.dumps(event).encode("utf-8"))
    producer.flush()
    print(f"Sent: {event}")
    time.sleep(10)

    i+=1
