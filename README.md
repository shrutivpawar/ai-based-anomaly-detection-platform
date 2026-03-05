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
