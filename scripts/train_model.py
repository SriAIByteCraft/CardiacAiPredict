"""
Model Training and Comparative Experiments Runner.
Trains the StackingClassifier ensemble, compares base models, balancing methods,
and dimensionality reduction techniques, saving all model artifacts and evaluation metrics.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from ml.train_pipeline import train_and_evaluate_full_system

def main():
    print("=" * 70)
    print("HEART DISEASE PREDICTION - STACKING ENSEMBLE TRAINING PIPELINE")
    print("=" * 70)
    artifacts_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend", "ml", "artifacts"))
    
    results = train_and_evaluate_full_system(artifacts_dir=artifacts_dir)
    
    print("\n" + "=" * 70)
    print("TRAINING AND EVALUATION COMPLETE")
    print("=" * 70)
    metrics = results["test_metrics"]
    print(f"Accuracy:    {metrics['accuracy']:.4f}")
    print(f"Precision:   {metrics['precision']:.4f}")
    print(f"Recall:      {metrics['recall']:.4f} (Sensitivity)")
    print(f"Specificity: {metrics['specificity']:.4f}")
    print(f"F1-Score:    {metrics['f1_score']:.4f}")
    if "roc_auc" in metrics and metrics["roc_auc"] is not None:
        print(f"ROC-AUC:     {metrics['roc_auc']:.4f}")
    print(f"Artifacts:   {artifacts_dir}")
    print("=" * 70)

if __name__ == "__main__":
    main()
