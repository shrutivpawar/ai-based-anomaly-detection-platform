import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib

# 1. Load Data
df = pd.read_csv("data/human_vital_signs_dataset_2024.csv")
features = ['Heart Rate', 'Respiratory Rate', 'Body Temperature', 
            'Oxygen Saturation', 'Systolic Blood Pressure', 
            'Diastolic Blood Pressure', 'Derived_HRV', 'Derived_MAP']
data = df[features].values

# 2. Scale
scaler = StandardScaler()
data_scaled = scaler.fit_transform(data)

# 3. Train Autoencoder (Deep Learning)
input_dim = data_scaled.shape[1]
model = models.Sequential([
    layers.Input(shape=(input_dim,)),
    layers.Dense(16, activation='relu'),
    layers.Dense(8, activation='relu'),
    layers.Dense(16, activation='relu'),
    layers.Dense(input_dim, activation='linear')
])
model.compile(optimizer='adam', loss='mse')
print("Training Autoencoder...")
model.fit(data_scaled, data_scaled, epochs=5, batch_size=32, verbose=0)

# 4. Train Isolation Forest (Machine Learning)
print("Training Isolation Forest...")
iso_forest = IsolationForest(n_estimators=100, contamination=0.01, random_state=42)
iso_forest.fit(data_scaled)

# 5. SAVE EVERYTHING
model.save('models/autoencoder.keras')
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(iso_forest, 'models/isolation_forest.pkl')

print("\n✅ All 3 files saved in models/ folder!")