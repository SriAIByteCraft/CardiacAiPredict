"""
Model Evaluation and Diagnostics Reporting script.
Reads generated model metrics and comparison results and prints structured summary.
"""
import sys
import os
import json

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "ml", "artifacts"))
    metrics_path = os.path.join(base_dir, "model_metrics.json")
    comp_path = os.path.join(base_dir, "model_comparison.json")

    print("=" * 70)
    print("HEART DISEASE PREDICTION - MODEL EVALUATION SUMMARY")
    print("=" * 70)

    if not os.path.exists(metrics_path):
        print(f"Error: Metrics file not found at {metrics_path}. Run `python scripts/train_model.py` first.")
        sys.exit(1)

    with open(metrics_path, "r") as f:
        meta = json.load(f)

    test_metrics = meta.get("test_metrics", {})
    print(f"Model Name:    {meta.get('model_name')}")
    print(f"Version:       {meta.get('version')}")
    print(f"Trained At:    {meta.get('trained_at')}")
    print(f"Dataset:       {meta.get('dataset')}")
    print("-" * 70)
    print(f"Test Accuracy:    {test_metrics.get('accuracy')}")
    print(f"Test Precision:   {test_metrics.get('precision')}")
    print(f"Test Recall:      {test_metrics.get('recall')}")
    print(f"Test Specificity: {test_metrics.get('specificity')}")
    print(f"Test F1-Score:    {test_metrics.get('f1_score')}")
    print(f"Test ROC-AUC:     {test_metrics.get('roc_auc')}")
    print(f"Confusion Matrix: {test_metrics.get('confusion_matrix', {}).get('matrix')}")
    print("=" * 70)

    if os.path.exists(comp_path):
        with open(comp_path, "r") as f:
            comp = json.load(f)
        print("\nCLASSIFIER COMPARISON (5-Fold Stratified CV):")
        for m in comp.get("models_comparison", []):
            print(f" - {m['model_name']:20s} | Acc: {m['accuracy']:.4f} | F1: {m['f1_score']:.4f} | AUC: {m['roc_auc']:.4f}")

        print("\nBALANCING TECHNIQUES COMPARISON:")
        for b in comp.get("balancing_comparison", []):
            print(f" - {b['technique']:32s} | Acc: {b['accuracy']:.4f} | Rec: {b['recall']:.4f} | AUC: {b['roc_auc']:.4f}")

        print("\nDIMENSIONALITY REDUCTION COMPARISON:")
        for r in comp.get("reduction_comparison", []):
            print(f" - {r['technique']:32s} | Acc: {r['accuracy']:.4f} | Rec: {r['recall']:.4f} | AUC: {r['roc_auc']:.4f}")
    print("=" * 70)

if __name__ == "__main__":
    main()
