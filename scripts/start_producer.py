import json
import time
import random
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

def generate_vitals():
    # Occasionally generate an anomaly (High HR or Low SpO2)
    is_anomaly = random.random() > 0.95 
    
    return {
        "Patient ID": random.randint(101, 105),
        "Heart Rate": random.uniform(120, 160) if is_anomaly else random.uniform(60, 100),
        "Respiratory Rate": random.uniform(12, 20),
        "Body Temperature": random.uniform(36.5, 37.5),
        "Oxygen Saturation": random.uniform(85, 92) if is_anomaly else random.uniform(95, 100),
        "Systolic Blood Pressure": random.uniform(110, 140),
        "Diastolic Blood Pressure": random.uniform(70, 90),
        "Derived_HRV": random.uniform(30, 70),
        "Derived_MAP": random.uniform(80, 100)
    }

print("📡 Producer started. Sending patient data to Kafka...")
while True:
    data = generate_vitals()
    producer.send('patient-vitals', value=data)
    time.sleep(1) # Send one reading per second