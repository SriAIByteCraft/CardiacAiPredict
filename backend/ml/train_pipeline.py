"""
End-to-End Training, Cross-Validation, Comparative Experiments, and Evaluation Pipeline.
Compares:
1. Individual Base Models vs Stacking Ensemble
2. Balancing Techniques: None, SMOTE, Undersampling, Class Weighting
3. Dimensionality Reduction: None, PCA, SelectKBest
Saves fitted artifact, metrics JSON, and comparative analysis.
"""
import os
import json
import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timezone

from sklearn.pipeline import Pipeline
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.decomposition import PCA
from sklearn.feature_selection import SelectKBest, f_classif

from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

from .data_loader import load_heart_data, split_dataset, FEATURE_COLUMNS
from .preprocessor import create_preprocessor
from .stacking_model import build_stacking_classifier, get_base_models
from .evaluate import evaluate_classification, plot_confusion_matrix, plot_roc_curve
from .explainability import compute_model_feature_importance

def run_experiments(X_train, y_train, cv=5, random_state=42):
    """
    Evaluates individual models, balancing strategies, and dimensionality reduction
    using Stratified 5-Fold Cross-Validation on training data only.
    """
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc"
    }

    results = {
        "models_comparison": [],
        "balancing_comparison": [],
        "reduction_comparison": []
    }

    # 1. Base Classifiers vs Stacking Ensemble Comparison
    preprocessor = create_preprocessor()
    candidate_models = get_base_models(random_state=random_state)
    candidate_models["stacking_ensemble"] = build_stacking_classifier(random_state=random_state, cv=3)

    for name, clf in candidate_models.items():
        pipe = Pipeline([
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        cv_res = cross_validate(pipe, X_train, y_train, cv=skf, scoring=scoring, n_jobs=-1)
        results["models_comparison"].append({
            "model_name": name,
            "accuracy": round(float(np.mean(cv_res["test_accuracy"])), 4),
            "precision": round(float(np.mean(cv_res["test_precision"])), 4),
            "recall": round(float(np.mean(cv_res["test_recall"])), 4),
            "f1_score": round(float(np.mean(cv_res["test_f1"])), 4),
            "roc_auc": round(float(np.mean(cv_res["test_roc_auc"])), 4)
        })

    # 2. Balancing Techniques Comparison (using Stacking Model)
    # Baseline (None)
    pipe_base = ImbPipeline([
        ("preprocessor", create_preprocessor()),
        ("classifier", build_stacking_classifier(random_state=random_state, cv=3))
    ])
    cv_none = cross_validate(pipe_base, X_train, y_train, cv=skf, scoring=scoring, n_jobs=-1)
    results["balancing_comparison"].append({
        "technique": "Baseline (No Resampling)",
        "accuracy": round(float(np.mean(cv_none["test_accuracy"])), 4),
        "recall": round(float(np.mean(cv_none["test_recall"])), 4),
        "f1_score": round(float(np.mean(cv_none["test_f1"])), 4),
        "roc_auc": round(float(np.mean(cv_none["test_roc_auc"])), 4)
    })

    # SMOTE
    pipe_smote = ImbPipeline([
        ("preprocessor", create_preprocessor()),
        ("sampler", SMOTE(random_state=random_state)),
        ("classifier", build_stacking_classifier(random_state=random_state, cv=3))
    ])
    cv_smote = cross_validate(pipe_smote, X_train, y_train, cv=skf, scoring=scoring, n_jobs=-1)
    results["balancing_comparison"].append({
        "technique": "SMOTE (Oversampling)",
        "accuracy": round(float(np.mean(cv_smote["test_accuracy"])), 4),
        "recall": round(float(np.mean(cv_smote["test_recall"])), 4),
        "f1_score": round(float(np.mean(cv_smote["test_f1"])), 4),
        "roc_auc": round(float(np.mean(cv_smote["test_roc_auc"])), 4)
    })

    # Random Undersampling
    pipe_rus = ImbPipeline([
        ("preprocessor", create_preprocessor()),
        ("sampler", RandomUnderSampler(random_state=random_state)),
        ("classifier", build_stacking_classifier(random_state=random_state, cv=3))
    ])
    cv_rus = cross_validate(pipe_rus, X_train, y_train, cv=skf, scoring=scoring, n_jobs=-1)
    results["balancing_comparison"].append({
        "technique": "Random Undersampling",
        "accuracy": round(float(np.mean(cv_rus["test_accuracy"])), 4),
        "recall": round(float(np.mean(cv_rus["test_recall"])), 4),
        "f1_score": round(float(np.mean(cv_rus["test_f1"])), 4),
        "roc_auc": round(float(np.mean(cv_rus["test_roc_auc"])), 4)
    })

    # Class Weighting
    pipe_weighted = ImbPipeline([
        ("preprocessor", create_preprocessor()),
        ("classifier", build_stacking_classifier(random_state=random_state, cv=3, class_weight="balanced"))
    ])
    cv_wt = cross_validate(pipe_weighted, X_train, y_train, cv=skf, scoring=scoring, n_jobs=-1)
    results["balancing_comparison"].append({
        "technique": "Class Weighting (Cost-Sensitive)",
        "accuracy": round(float(np.mean(cv_wt["test_accuracy"])), 4),
        "recall": round(float(np.mean(cv_wt["test_recall"])), 4),
        "f1_score": round(float(np.mean(cv_wt["test_f1"])), 4),
        "roc_auc": round(float(np.mean(cv_wt["test_roc_auc"])), 4)
    })

    # 3. Dimensionality Reduction Comparison (Stacking Model)
    # Full Features (Baseline)
    results["reduction_comparison"].append({
        "technique": "Full Features (13 raw attributes)",
        "components_or_features": 13,
        "accuracy": results["balancing_comparison"][0]["accuracy"],
        "recall": results["balancing_comparison"][0]["recall"],
        "f1_score": results["balancing_comparison"][0]["f1_score"],
        "roc_auc": results["balancing_comparison"][0]["roc_auc"]
    })

    # PCA (10 components)
    pipe_pca = Pipeline([
        ("preprocessor", create_preprocessor()),
        ("pca", PCA(n_components=10, random_state=random_state)),
        ("classifier", build_stacking_classifier(random_state=random_state, cv=3))
    ])
    cv_pca = cross_validate(pipe_pca, X_train, y_train, cv=skf, scoring=scoring, n_jobs=-1)
    results["reduction_comparison"].append({
        "technique": "PCA (10 Principal Components)",
        "components_or_features": 10,
        "accuracy": round(float(np.mean(cv_pca["test_accuracy"])), 4),
        "recall": round(float(np.mean(cv_pca["test_recall"])), 4),
        "f1_score": round(float(np.mean(cv_pca["test_f1"])), 4),
        "roc_auc": round(float(np.mean(cv_pca["test_roc_auc"])), 4)
    })

    # SelectKBest (10 features)
    pipe_kbest = Pipeline([
        ("preprocessor", create_preprocessor()),
        ("kbest", SelectKBest(score_func=f_classif, k=10)),
        ("classifier", build_stacking_classifier(random_state=random_state, cv=3))
    ])
    cv_kbest = cross_validate(pipe_kbest, X_train, y_train, cv=skf, scoring=scoring, n_jobs=-1)
    results["reduction_comparison"].append({
        "technique": "SelectKBest (ANOVA F-value Top 10)",
        "components_or_features": 10,
        "accuracy": round(float(np.mean(cv_kbest["test_accuracy"])), 4),
        "recall": round(float(np.mean(cv_kbest["test_recall"])), 4),
        "f1_score": round(float(np.mean(cv_kbest["test_f1"])), 4),
        "roc_auc": round(float(np.mean(cv_kbest["test_roc_auc"])), 4)
    })

    return results

def train_and_evaluate_full_system(artifacts_dir=None, random_state=42):
    """
    Main training execution function.
    1. Loads dataset
    2. Runs comparison experiments
    3. Fits best full pipeline (preprocessor + stacking classifier)
    4. Evaluates on held-out test set
    5. Saves model artifact, JSON metrics, and visual plots
    """
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if artifacts_dir is None:
        artifacts_dir = os.path.join(base_dir, "ml", "artifacts")
    os.makedirs(artifacts_dir, exist_ok=True)

    print("Loading UCI Heart Disease dataset...")
    df = load_heart_data()
    X_train, X_test, y_train, y_test = split_dataset(df, test_size=0.2, random_state=random_state)
    print(f"Data split: Train {X_train.shape}, Test {X_test.shape}")

    # Run cross-validation comparisons
    print("Running comparative cross-validation experiments...")
    comparison_results = run_experiments(X_train, y_train, cv=5, random_state=random_state)

    # Train final full Stacking Pipeline
    print("Fitting final Stacking Ensemble Pipeline...")
    final_pipeline = Pipeline([
        ("preprocessor", create_preprocessor()),
        ("classifier", build_stacking_classifier(random_state=random_state, cv=5))
    ])

    final_pipeline.fit(X_train, y_train)

    # Test set evaluation
    print("Evaluating final model on held-out test set...")
    y_pred = final_pipeline.predict(X_test)
    y_prob = final_pipeline.predict_proba(X_test)[:, 1]

    test_metrics = evaluate_classification(y_test, y_pred, y_prob)
    print(f"Test Set Accuracy: {test_metrics['accuracy']:.4f}, ROC-AUC: {test_metrics.get('roc_auc', 0):.4f}")

    # Feature importances / explainability
    print("Computing feature importance analysis...")
    importance_data = compute_model_feature_importance(
        final_pipeline, X_test, y_test, top_n=10, random_state=random_state
    )

    # Save artifacts
    model_file = os.path.join(artifacts_dir, "stacking_heart_model.joblib")
    metrics_file = os.path.join(artifacts_dir, "model_metrics.json")
    comparison_file = os.path.join(artifacts_dir, "model_comparison.json")

    timestamp = datetime.now(timezone.utc).isoformat()
    metadata = {
        "model_name": "StackingClassifier (LR + RF + SVM -> Meta LR)",
        "version": "1.0.0",
        "trained_at": timestamp,
        "dataset": "UCI Cleveland Heart Disease",
        "sample_counts": {
            "total": int(len(df)),
            "train": int(len(X_train)),
            "test": int(len(X_test)),
            "disease_positive": int(df["target"].sum()),
            "disease_negative": int((df["target"] == 0).sum())
        },
        "test_metrics": test_metrics,
        "explainability": importance_data
    }

    # Save joblib bundle
    joblib.dump({"pipeline": final_pipeline, "metadata": metadata}, model_file)
    print(f"Saved model pipeline artifact: {model_file}")

    # Save metrics JSON
    with open(metrics_file, "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved metrics JSON: {metrics_file}")

    # Save comparison JSON
    with open(comparison_file, "w") as f:
        json.dump(comparison_results, f, indent=2)
    print(f"Saved comparison JSON: {comparison_file}")

    # Generate plots
    cm_plot_path = os.path.join(artifacts_dir, "confusion_matrix.png")
    plot_confusion_matrix(test_metrics["confusion_matrix"]["matrix"], cm_plot_path)

    roc_plot_path = os.path.join(artifacts_dir, "roc_curve.png")
    plot_roc_curve(y_test, y_prob, roc_plot_path)
    print(f"Saved evaluation plots in {artifacts_dir}")

    return {
        "model_file": model_file,
        "metrics_file": metrics_file,
        "comparison_file": comparison_file,
        "test_metrics": test_metrics,
        "comparison_results": comparison_results
    }

if __name__ == "__main__":
    train_and_evaluate_full_system()
