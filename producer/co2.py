import os
os.environ["MH_Z19_SERIAL_DEVICE"] = "/dev/ttyAMA0"  # MUST come before importing mh_z19

from confluent_kafka import Producer
import mh_z19
import json
import time
from datetime import datetime

producer = Producer({
    'bootstrap.servers': '192.168.0.113:29092'
})

while True:
    try:
        values = []
        for _ in range(10):
            result = mh_z19.read()
            if result and "co2" in result:
                values.append(result["co2"])
            time.sleep(0.5)

        if values:
            avg_co2 = sum(values) / len(values)
            event = {
                "timestamp": datetime.utcnow().isoformat(),
                "location": "amsterdam.indoor",
                "co2_ppm": round(avg_co2, 1)
            }
            producer.produce("indoor.co2", json.dumps(event).encode("utf-8"))
            producer.flush()
            print("Averaged CO₂ event:", event)
        else:
            print("No valid CO₂ readings collected.")

    except Exception as e:
        print("Error:", e)

