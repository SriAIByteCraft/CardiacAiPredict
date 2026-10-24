"""
Dataset download and preparation script for UCI Heart Disease (Cleveland) dataset.
Source: UCI Machine Learning Repository
https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data
"""
import os
import urllib.request
import pandas as pd
import numpy as np

UCI_CLEVELAND_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
COLUMN_NAMES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", 
    "restecg", "thalach", "exang", "oldpeak", "slope", 
    "ca", "thal", "target"
]

def prepare_dataset(base_dir=None):
    if base_dir is None:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    raw_dir = os.path.join(base_dir, "data", "raw")
    processed_dir = os.path.join(base_dir, "data", "processed")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)

    raw_data_file = os.path.join(raw_dir, "processed.cleveland.data")
    csv_file = os.path.join(raw_dir, "heart_disease_uci.csv")

    # Step 1: Download raw data if not present
    if not os.path.exists(raw_data_file):
        print(f"Downloading UCI Cleveland dataset from {UCI_CLEVELAND_URL}...")
        urllib.request.urlretrieve(UCI_CLEVELAND_URL, raw_data_file)
        print("Download complete.")
    else:
        print(f"Raw data already exists at: {raw_data_file}")

    # Step 2: Parse raw comma-separated data
    print("Reading and parsing dataset...")
    df = pd.read_csv(raw_data_file, header=None, names=COLUMN_NAMES, na_values="?")

    print(f"Raw shape: {df.shape}")
    print(f"Missing values count:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

    # Step 3: Handle target (UCI target: 0 = absent, 1,2,3,4 = present)
    # Binarize: 0 -> 0 (No Heart Disease), >0 -> 1 (Heart Disease Present)
    df["target"] = (df["target"] > 0).astype(int)

    # Save standardized CSV
    df.to_csv(csv_file, index=False)
    print(f"Standardized dataset saved to: {csv_file}")

    # Step 4: Class distribution check
    counts = df["target"].value_counts().to_dict()
    print(f"Target distribution: {counts} (0: No disease, 1: Disease)")
    return csv_file

if __name__ == "__main__":
    prepare_dataset()
