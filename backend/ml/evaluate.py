"""
Evaluation metrics and plotting utilities for Heart Disease classification.
Calculates Accuracy, Precision, Recall/Sensitivity, Specificity, F1-Score, ROC-AUC,
Confusion Matrix, and Calibration.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
    precision_recall_curve,
    brier_score_loss
)

def evaluate_classification(y_true, y_pred, y_prob=None):
    """
    Computes standard healthcare evaluation metrics.
    """
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    
    accuracy = float(accuracy_score(y_true, y_pred))
    precision = float(precision_score(y_true, y_pred, zero_division=0))
    recall = float(recall_score(y_true, y_pred, zero_division=0))  # Sensitivity
    specificity = float(tn / (tn + fp)) if (tn + fp) > 0 else 0.0
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    metrics = {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "sensitivity": round(recall, 4),
        "specificity": round(specificity, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp),
            "matrix": [[int(tn), int(fp)], [int(fn), int(tp)]]
        }
    }

    if y_prob is not None:
        try:
            auc = float(roc_auc_score(y_true, y_prob))
            metrics["roc_auc"] = round(auc, 4)
            brier = float(brier_score_loss(y_true, y_prob))
            metrics["brier_score"] = round(brier, 4)

            fpr, tpr, _ = roc_curve(y_true, y_prob)
            precisions, recalls, _ = precision_recall_curve(y_true, y_prob)
            
            # Sample curve points for lightweight JSON transport
            step = max(1, len(fpr) // 25)
            metrics["roc_curve"] = {
                "fpr": [round(float(x), 4) for x in fpr[::step]],
                "tpr": [round(float(y), 4) for y in tpr[::step]]
            }
            metrics["pr_curve"] = {
                "precision": [round(float(p), 4) for p in precisions[::step]],
                "recall": [round(float(r), 4) for r in recalls[::step]]
            }
        except Exception as e:
            metrics["roc_auc"] = None
            metrics["roc_auc_error"] = str(e)

    return metrics

def plot_confusion_matrix(cm_matrix, output_path, title="Confusion Matrix"):
    """Saves styled Confusion Matrix visualization."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm_matrix,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["No Disease (0)", "Disease (1)"],
        yticklabels=["No Disease (0)", "Disease (1)"],
        cbar=True,
        ax=ax
    )
    ax.set_title(title, fontsize=14, pad=12, fontweight="bold")
    ax.set_xlabel("Predicted Label", fontsize=11)
    ax.set_ylabel("True Label", fontsize=11)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close(fig)

def plot_roc_curve(y_true, y_prob, output_path, title="ROC Curve"):
    """Saves styled ROC Curve plot."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    auc_val = roc_auc_score(y_true, y_prob)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(fpr, tpr, color="#0ea5e9", lw=2.5, label=f"ROC (AUC = {auc_val:.3f})")
    ax.plot([0, 1], [0, 1], color="#94a3b8", lw=1.5, linestyle="--", label="Chance")
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate (1 - Specificity)", fontsize=11)
    ax.set_ylabel("True Positive Rate (Sensitivity / Recall)", fontsize=11)
    ax.set_title(title, fontsize=14, pad=12, fontweight="bold")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close(fig)
