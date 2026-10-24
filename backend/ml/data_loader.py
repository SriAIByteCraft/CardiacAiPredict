"""
Data Loader and Dataset Schema Definitions for UCI Cleveland Heart Disease Dataset.
"""
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

COLUMN_NAMES = [
    "age", "sex", "cp", "trestbps", "chol", "fbs", 
    "restecg", "thalach", "exang", "oldpeak", "slope", 
    "ca", "thal", "target"
]

FEATURE_COLUMNS = [col for col in COLUMN_NAMES if col != "target"]

NUMERIC_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL_FEATURES = ["sex", "cp", "fbs", "restecg", "exang", "slope", "ca", "thal"]

FEATURE_METADATA = {
    "age": {
        "type": "numeric",
        "description": "Age in years",
        "min": 18,
        "max": 100,
        "default": 54
    },
    "sex": {
        "type": "categorical",
        "description": "Biological sex",
        "options": {
            0: "Female",
            1: "Male"
        },
        "default": 1
    },
    "cp": {
        "type": "categorical",
        "description": "Chest pain type",
        "options": {
            1: "Typical Angina",
            2: "Atypical Angina",
            3: "Non-anginal Pain",
            4: "Asymptomatic"
        },
        "default": 4
    },
    "trestbps": {
        "type": "numeric",
        "description": "Resting blood pressure in mm Hg (admission)",
        "min": 80,
        "max": 220,
        "default": 130
    },
    "chol": {
        "type": "numeric",
        "description": "Serum cholesterol in mg/dl",
        "min": 100,
        "max": 600,
        "default": 240
    },
    "fbs": {
        "type": "categorical",
        "description": "Fasting blood sugar > 120 mg/dl",
        "options": {
            0: "False (<= 120 mg/dl)",
            1: "True (> 120 mg/dl)"
        },
        "default": 0
    },
    "restecg": {
        "type": "categorical",
        "description": "Resting electrocardiographic results",
        "options": {
            0: "Normal",
            1: "ST-T Wave Abnormality",
            2: "Left Ventricular Hypertrophy"
        },
        "default": 0
    },
    "thalach": {
        "type": "numeric",
        "description": "Maximum heart rate achieved during exercise",
        "min": 60,
        "max": 220,
        "default": 150
    },
    "exang": {
        "type": "categorical",
        "description": "Exercise induced angina",
        "options": {
            0: "No",
            1: "Yes"
        },
        "default": 0
    },
    "oldpeak": {
        "type": "numeric",
        "description": "ST depression induced by exercise relative to rest",
        "min": 0.0,
        "max": 7.0,
        "default": 1.0
    },
    "slope": {
        "type": "categorical",
        "description": "Slope of the peak exercise ST segment",
        "options": {
            1: "Upsloping",
            2: "Flat",
            3: "Downsloping"
        },
        "default": 1
    },
    "ca": {
        "type": "categorical",
        "description": "Number of major vessels (0-3) colored by flourosopy",
        "options": {
            0: "0 vessels",
            1: "1 vessel",
            2: "2 vessels",
            3: "3 vessels"
        },
        "default": 0
    },
    "thal": {
        "type": "categorical",
        "description": "Thalassemia blood disorder result",
        "options": {
            3: "Normal",
            6: "Fixed Defect",
            7: "Reversible Defect"
        },
        "default": 3
    }
}

def resolve_data_paths():
    """Finds raw data CSV or download source."""
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    csv_file = os.path.join(base_dir, "data", "raw", "heart_disease_uci.csv")
    raw_dat_file = os.path.join(base_dir, "data", "raw", "processed.cleveland.data")
    return csv_file, raw_dat_file

def load_heart_data(csv_path=None):
    """
    Loads UCI Heart Disease Cleveland dataset.
    Ensures missing values ('?') are handled and target is binary.
    """
    default_csv, default_raw = resolve_data_paths()
    path = csv_path or default_csv

    if not os.path.exists(path):
        if os.path.exists(default_raw):
            # Parse from raw .data file
            df = pd.read_csv(default_raw, header=None, names=COLUMN_NAMES, na_values="?")
            df["target"] = (df["target"] > 0).astype(int)
            os.makedirs(os.path.dirname(default_csv), exist_ok=True)
            df.to_csv(default_csv, index=False)
            return df
        raise FileNotFoundError(
            f"Dataset not found at {path}. Run `python scripts/download_dataset.py` first."
        )

    df = pd.read_csv(path, na_values="?")
    # Ensure standard columns
    missing_cols = set(COLUMN_NAMES) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {missing_cols}")

    # Ensure target is binary (0: absence, 1: presence)
    if df["target"].max() > 1:
        df["target"] = (df["target"] > 0).astype(int)

    return df

def split_dataset(df, test_size=0.2, random_state=42):
    """
    Performs stratified split on the dataset into training and test sets.
    """
    X = df[FEATURE_COLUMNS].copy()
    y = df["target"].copy()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    return X_train, X_test, y_train, y_test
