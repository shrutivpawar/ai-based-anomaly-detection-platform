import psycopg2
try:
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="root", 
                            host="localhost", port="5432", sslmode='disable')
    cur = conn.cursor()
    cur.execute("INSERT INTO anomaly_logs (patient_id, anomaly_score, severity) VALUES (1, 0.5, 'LOW')")
    conn.commit()
    print("✅ Connection and Insert Worked!")
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Connection Failed: {e}")