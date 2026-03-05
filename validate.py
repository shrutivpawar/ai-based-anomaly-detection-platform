import pandas as pd

# Load dataset (make sure the file is in the 'data' folder)
file_path = "data/human_vital_signs_dataset_2024.csv"

try:
    df = pd.read_csv(file_path)
    print("--- 🩺 Dataset Validation Report ---")

    # 1. Dataset shape and size
    print(f"Total Records: {df.shape[0]}")
    print(f"Total Features: {df.shape[1]}")

    # 2. Availability of vital sign features
    # These match the columns in the Kaggle dataset
    required = ['Heart Rate', 'Body Temperature', 'Oxygen Saturation', 'Systolic Blood Pressure']
    print(f"Checking for features: {required}")

    # 3. Absence of missing or corrupted values
    missing = df.isnull().sum().sum()
    print(f"Total Missing Values: {missing}")

    # 4. Consistency of numerical ranges (Logic Check)
    print("\nRange Check (Min/Max):")
    stats = df.describe().loc[['min', 'max']]
    print(stats)

    if missing == 0:
        print("\n✅ Success: Data is clean and ready for AI training.")
    else:
        print(f"\n⚠️ Warning: Found {missing} missing values. Consider df.dropna().")

except FileNotFoundError:
    print(f"❌ Error: Could not find the file at {file_path}. Check your folder names!")