"""
Model Explainability and Feature Importance Module.
Extracts model-agnostic permutation importances or meta-model coefficients.
Includes medical/research disclaimers explicitly differentiating statistical correlation from causal etiology.
"""
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance

DISCLAIMER_TEXT = (
    "EDUCATIONAL AND RESEARCH USE ONLY: Feature contribution scores reflect statistical associations "
    "learned by the machine learning algorithm on the specific dataset sample. They do NOT establish medical "
    "causation, disease etiology, or individual clinical diagnosis. Never alter medications, lifestyle, "
    "or medical treatment based solely on these algorithmic scores."
)

def compute_model_feature_importance(pipeline, X_val, y_val, top_n=10, random_state=42):
    """
    Computes permutation importance on validation data through the fitted pipeline.
    Returns sorted list of features with importance means and standard deviations.
    """
    try:
        # Compute permutation importance
        perm_res = permutation_importance(
            pipeline,
            X_val,
            y_val,
            n_repeats=5,
            random_state=random_state,
            scoring="roc_auc"
        )

        features = list(X_val.columns)
        importances = []

        for idx in np.argsort(perm_res.importances_mean)[::-1]:
            feat_name = features[idx]
            mean_imp = float(perm_res.importances_mean[idx])
            std_imp = float(perm_res.importances_std[idx])
            
            importances.append({
                "feature": feat_name,
                "importance_mean": round(mean_imp, 4),
                "importance_std": round(std_imp, 4)
            })

        return {
            "method": "Permutation Importance (held-out ROC-AUC drop)",
            "top_features": importances[:top_n],
            "disclaimer": DISCLAIMER_TEXT
        }

    except Exception as e:
        return {
            "method": "Permutation Importance",
            "top_features": [],
            "error": str(e),
            "disclaimer": DISCLAIMER_TEXT
        }

def get_instance_explanation(input_dict, feature_importance_summary):
    """
    Provides context for a single patient prediction relative to prominent features.
    """
    top_factors = []
    if feature_importance_summary and "top_features" in feature_importance_summary:
        for item in feature_importance_summary["top_features"][:5]:
            feat = item["feature"]
            val = input_dict.get(feat)
            top_factors.append({
                "feature": feat,
                "observed_value": val,
                "global_importance": item["importance_mean"]
            })

    return {
        "factors": top_factors,
        "disclaimer": DISCLAIMER_TEXT
    }
