"""
Class Balancing Techniques for Imbalanced Heart Disease Classification.
Provides:
1. Baseline (No resampling)
2. SMOTE (Synthetic Minority Over-sampling Technique)
3. Random Undersampling (RandomUnderSampler)
4. Class Weighting (balanced parameter configuration)
"""
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

BALANCING_TECHNIQUES = {
    "none": "No Resampling (Baseline)",
    "smote": "SMOTE (Oversampling)",
    "undersampling": "Random Undersampling",
    "class_weight": "Cost-Sensitive / Class Weighting"
}

def get_balancing_sampler(method_name="none", random_state=42):
    """
    Returns an imblearn resampler object or None.
    Applies only during training pipeline to prevent leakage.
    """
    normalized_name = (method_name or "none").lower()
    
    if normalized_name in ["smote", "oversampling"]:
        return SMOTE(random_state=random_state)
    elif normalized_name in ["undersampling", "under_sampling", "rus"]:
        return RandomUnderSampler(random_state=random_state)
    elif normalized_name in ["none", "baseline", "class_weight"]:
        return None
    else:
        raise ValueError(
            f"Unknown balancing technique: '{method_name}'. "
            f"Allowed: {list(BALANCING_TECHNIQUES.keys())}"
        )

def apply_training_balance(X_train, y_train, method_name="none", random_state=42):
    """
    Safely resamples training set features and target.
    Must NEVER be called on validation or test sets.
    """
    sampler = get_balancing_sampler(method_name, random_state=random_state)
    if sampler is None:
        return X_train, y_train, {"method": method_name, "resampled": False}
    
    X_res, y_res = sampler.fit_resample(X_train, y_train)
    metadata = {
        "method": method_name,
        "resampled": True,
        "original_counts": dict(zip(*np.unique(y_train, return_counts=True))) if hasattr(y_train, "__iter__") else {},
        "resampled_counts": dict(zip(*np.unique(y_res, return_counts=True))) if hasattr(y_res, "__iter__") else {}
    }
    return X_res, y_res, metadata
