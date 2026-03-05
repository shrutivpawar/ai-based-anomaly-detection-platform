from flask import Flask, render_template, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import threading

app = Flask(__name__)

# Database connection helper
def get_db_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="root", 
        host="localhost",
        port="5432",
        sslmode='disable' # Fixes the SSL error from your screenshot
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/alerts')
def get_alerts():
    try:
        conn = get_db_connection()
        # RealDictCursor makes the data look like JSON automatically
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Fetch the last 50 anomalies from the database
        query = """
            SELECT 
                timestamp, 
                patient_id as "Patient ID", 
                anomaly_score as "Score", 
                severity, 
                heart_rate as "Heart Rate", 
                spo2 as "Oxygen Saturation", 
                temperature as "Body Temperature", 
                systolic_bp as "Systolic Blood Pressure", 
                diastolic_bp as "Diastolic Blood Pressure"
            FROM anomaly_logs 
            ORDER BY timestamp DESC 
            LIMIT 50;
        """
        cur.execute(query)
        alerts = cur.fetchall()
        
        # Format the timestamp for the frontend
        for alert in alerts:
            alert['timestamp'] = alert['timestamp'].strftime("%Y-%m-%d %H:%M:%S")
            
        cur.close()
        conn.close()
        return jsonify(alerts)
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify([])

if __name__ == '__main__':
    # We remove the threading logic here because streaming_consumer_ml.py 
    # is now handling the DB writes. app.py just reads them.
    app.run(debug=True, port=5000)