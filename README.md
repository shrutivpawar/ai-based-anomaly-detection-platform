# 🏥 AI-Based Real-Time Health Anomaly Detection Platform

A robust, full-stack monitoring system that uses **Machine Learning** (Autoencoders + Isolation Forests) to detect life-threatening anomalies in real-time patient vitals. Data is streamed via **Apache Kafka** and persisted in **PostgreSQL**.



## 🚀 Features
* **Real-time Streaming**: Synthetic patient data generated and streamed via Kafka.
* **Ensemble AI**: Dual-model detection using Deep Learning (Autoencoders) and Statistical ML (Isolation Forest).
* **Persistent Logging**: Every detected anomaly is stored in a PostgreSQL database for historical analysis.
* **Live Dashboard**: A responsive UI built with Tailwind CSS and Chart.js to visualize vitals and risk scores.

---

## 🛠️ Tech Stack
* **Backend:** Python 3.10+, Flask, Apache Kafka, TensorFlow, Scikit-learn.
* **Database:** PostgreSQL 18.
* **Frontend:** HTML5, Tailwind CSS, Chart.js.
* **Environment:** VS Code, pgAdmin 4.

---

## 💻 Local Setup Instructions

### 1. Prerequisites
Ensure you have the following installed on your local machine:
* [Python 3.10+](https://www.python.org/downloads/)
* [Apache Kafka](https://kafka.apache.org/downloads)
* [PostgreSQL & pgAdmin 4](https://www.postgresql.org/download/)

### 2. Database Configuration
Open **pgAdmin 4**, connect to your server, and run the following SQL script to initialize the table:

```sql
CREATE TABLE anomaly_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    patient_id VARCHAR(50),
    anomaly_score DOUBLE PRECISION,
    severity VARCHAR(20),
    heart_rate DOUBLE PRECISION,
    spo2 DOUBLE PRECISION,
    temperature DOUBLE PRECISION,
    systolic_bp DOUBLE PRECISION,
    diastolic_bp DOUBLE PRECISION
);
```
### 3. Environment Setup
Clone the repository and set up a virtual environment in your terminal:

```
git clone [https://github.com/shrutivpawar/ai-based-anomaly-detection-platform.git](https://github.com/shrutivpawar/ai-based-anomaly-detection-platform.git)
cd ai-based-anomaly-detection-platform
```

Create and activate virtual environment
```
python -m venv venv
.\venv\Scripts\activate
```

Install dependencies
```
pip install -r requirements.txt
```
Running the Platform:
To view the project locally, open separate terminals in VS Code and run these components in order:

Start Zookeeper:
```
.\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
```

Start Kafka Broker:
```
$env:KAFKA_HEAP_OPTS = "-Xmx1G -Xms1G"; .\bin\windows\kafka-server-start.bat .\config\server.properties
```
Start Data Producer:
```
python scripts/start_producer.py
```

Start ML Consumer (Data Processor & DB Logger):
```
python scripts/streaming_consumer_ml.py
```

Start Flask Web Server:
```
python app/app.py
```

Access the Dashboard: Open your browser and go to http://127.0.0.1:5000

### 4. 📊 Project Structure
```
AI-BASED-ANOMALY/
├── app/
│   ├── templates/          # HTML files for the dashboard UI
│   └── app.py              # Flask application (API & Web Server)
├── data/
│   └── human_vital_signs_dataset_2024.csv  # Raw dataset for training/testing
├── models/                 # Saved Machine Learning artifacts
│   ├── autoencoder.keras   # Trained Deep Learning model
│   ├── isolation_forest.pkl # Trained Statistical ML model
│   ├── scaler.pkl          # Data normalization parameters
│   └── train_model.py      # Script to train and export models
├── notebooks/
│   └── EDA_and_Preprocessing.ipynb  # Data exploration & sequence creation
├── scripts/
│   └── start_producer.py   # Kafka Producer (Simulates real-time vitals)
├── venv/                   # Python Virtual Environment (Local only)
├── .gitignore              # Files to exclude from GitHub (venv, logs, etc.)
├── requirements.txt        # Project dependencies and libraries
├── streaming_consumer_ml.py # Kafka Consumer (AI Inference & Postgres Logger)
└── validate.py             # Script to verify system components
```
requirements.txt file:
```
# Web Framework & API
flask==3.0.0
flask-cors==4.0.0

# Database
psycopg2-binary==2.9.9

# Streaming
kafka-python==2.0.2

# Machine Learning & Data Processing
tensorflow==2.15.0
scikit-learn==1.3.2
pandas==2.1.4
numpy==1.26.2
joblib==1.3.2

# Utilities
python-dotenv==1.0.0
```

### 5. 🛡️ Troubleshooting
Postgres Connection: If you encounter an SSL error, ensure the connection string in app.py and streaming_consumer_ml.py includes sslmode=disable.

Kafka WMIC Error: If the Kafka server fails to start with a 'wmic' error, add C:\Windows\System32\wbem to your System Environment Path variables.

Empty Table: Verify that the Producer and Consumer are both running; the database will only populate when an anomaly is detected and processed.
