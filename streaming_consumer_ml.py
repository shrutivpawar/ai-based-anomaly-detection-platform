import json
import joblib
import numpy as np
import tensorflow as tf
from kafka import KafkaConsumer
from collections import deque
import psycopg2

# --- 1. Database Function (Define this BEFORE the loop) ---
def save_to_db(record, score, severity):
    try:
        conn = psycopg2.connect(
            dbname="postgres", 
            user="postgres", 
            password="root", 
            host="localhost", 
            port="5432",
            sslmode='disable'  # Added this to fix your SSL error
        )
        cur = conn.cursor()
        
        insert_query = """
        INSERT INTO anomaly_logs (patient_id, anomaly_score, severity, heart_rate, spo2, temperature, systolic_bp, diastolic_bp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        # We use .get() to avoid KeyErrors if a field is missing
        record_to_insert = (
            record['Patient ID'],
            float(score),
            severity,
            record['Heart Rate'],
            record['Oxygen Saturation'],
            record['Body Temperature'],
            record['Systolic Blood Pressure'],
            record['Diastolic Blood Pressure']
        )
        
        cur.execute(insert_query, record_to_insert)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Database Error: {e}")

# 1. Load the 3 components from Milestone 2 & 3
model = tf.keras.models.load_model('models/autoencoder.keras')
iso_forest = joblib.load('models/isolation_forest.pkl')
scaler = joblib.load('models/scaler.pkl')

# 2. Sliding Window Setup (Size 10 as per Milestone 3)
window_size = 10
vitals_window = deque(maxlen=window_size)

consumer = KafkaConsumer(
    'patient-vitals',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("🚀 Ensemble AI Consumer started. Monitoring for HIGH risk...")

for message in consumer:
    record = message.value
    # Features must match your training: HR, Resp, Temp, SpO2, Sys, Dia, HRV, MAP
    features = [
        record['Heart Rate'], record['Respiratory Rate'], record['Body Temperature'],
        record['Oxygen Saturation'], record['Systolic Blood Pressure'],
        record['Diastolic Blood Pressure'], record['Derived_HRV'], record['Derived_MAP']
    ]
    
    # Update sliding window
    vitals_window.append(features)
    
    if len(vitals_window) == window_size:
        # Scale the data
        current_data = scaler.transform([features])
        
        # MODEL 1: Autoencoder Reconstruction Error
        reconstruction = model.predict(current_data, verbose=0)
        auto_error = np.mean(np.square(current_data - reconstruction))
        
        # MODEL 2: Isolation Forest Score (1 is normal, -1 is anomaly)
        iso_score = iso_forest.decision_function(current_data)[0]
        
        # ENSEMBLE: Combine scores for Risk Classification
        # We flip iso_score so higher = more dangerous
        risk_score = (auto_error * 0.7) + (abs(iso_score) * 0.3)
        
        if risk_score > 0.8:
            severity = "🔴 HIGH"
        elif risk_score > 0.5:
            severity = "🟡 MEDIUM"
        else:
            severity = "🟢 LOW"
            
        print(f"Patient {record['Patient ID']} | Risk: {severity} | Score: {risk_score:.4f}")

        save_to_db(record, risk_score, severity)

