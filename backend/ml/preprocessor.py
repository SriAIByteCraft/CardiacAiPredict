"""
Preprocessing pipeline for Heart Disease dataset.
Handles missing values, scaling for continuous attributes, and one-hot encoding for categorical attributes.
"""
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from .data_loader import NUMERIC_FEATURES, CATEGORICAL_FEATURES

def create_preprocessor():
    """
    Creates a scikit-learn ColumnTransformer for preprocessing.
    - Numeric features: Median imputation + StandardScaler
    - Categorical features: Most frequent imputation + OneHotEncoder (ignoring unseen classes)
    """
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, NUMERIC_FEATURES),
            ("cat", cat_pipeline, CATEGORICAL_FEATURES)
        ],
        remainder="drop"
    )

    return preprocessor

def get_transformed_feature_names(preprocessor):
    """
    Retrieves human-readable feature names after ColumnTransformer fitting.
    """
    feature_names = []
    try:
        # scikit-learn 1.0+ get_feature_names_out
        feature_names = list(preprocessor.get_feature_names_out())
    except Exception:
        # Fallback if not fitted or older API
        feature_names = NUMERIC_FEATURES + [f"cat_{c}" for c in CATEGORICAL_FEATURES]
    return feature_names
