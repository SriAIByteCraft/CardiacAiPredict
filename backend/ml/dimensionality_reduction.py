"""
Dimensionality Reduction and Feature Selection Techniques.
Provides:
1. Baseline (Full feature set)
2. PCA (Principal Component Analysis with explained variance monitoring)
3. SelectKBest (ANOVA F-value feature selection)
"""
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif

REDUCTION_TECHNIQUES = {
    "none": "Full Features (Baseline)",
    "pca": "Principal Component Analysis (PCA)",
    "select_k_best": "Feature Selection (SelectKBest - ANOVA F-test)"
}

def get_reduction_step(method_name="none", n_components=10, k=10, random_state=42):
    """
    Returns a scikit-learn transformer step for dimensionality reduction or feature selection,
    or None if no reduction is requested.
    """
    normalized_name = (method_name or "none").lower()
    
    if normalized_name in ["none", "baseline"]:
        return None
    elif normalized_name == "pca":
        # Keep either specified components or variance ratio
        return PCA(n_components=n_components, random_state=random_state)
    elif normalized_name in ["select_k_best", "selectkbest", "kbest"]:
        return SelectKBest(score_func=f_classif, k=k)
    else:
        raise ValueError(
            f"Unknown dimensionality reduction technique: '{method_name}'. "
            f"Allowed: {list(REDUCTION_TECHNIQUES.keys())}"
        )
