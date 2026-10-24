"""
Model Metrics Record Model.
Stores training provenance, evaluation scores, and technique configurations in MongoDB.
"""
from datetime import datetime, timezone
from bson import ObjectId

class ModelMetricsRecord:
    """Represents a saved model performance evaluation snapshot."""

    @staticmethod
    def create_document(metadata: dict) -> dict:
        now = datetime.now(timezone.utc)
        return {
            "model_version": metadata.get("version", "1.0.0"),
            "model_name": metadata.get("model_name", "StackingClassifier"),
            "dataset_info": metadata.get("dataset", "UCI Cleveland Heart Disease"),
            "sample_counts": metadata.get("sample_counts", {}),
            "evaluation_metrics": metadata.get("test_metrics", {}),
            "balancing_technique": "Baseline (None) & SMOTE comparative evaluation",
            "dimensionality_reduction_method": "Full features baseline & PCA / SelectKBest comparison",
            "selected_features_count": 13,
            "training_timestamp": metadata.get("trained_at", now.isoformat()),
            "evaluation_timestamp": now.isoformat(),
            "explainability": metadata.get("explainability", {}),
            "created_at": now
        }

    @staticmethod
    def to_safe_dict(doc: dict) -> dict:
        if not doc:
            return {}
        rec_id = str(doc["_id"]) if "_id" in doc else None
        created_at = doc.get("created_at")
        return {
            "id": rec_id,
            "model_version": doc.get("model_version"),
            "model_name": doc.get("model_name"),
            "dataset_info": doc.get("dataset_info"),
            "sample_counts": doc.get("sample_counts"),
            "evaluation_metrics": doc.get("evaluation_metrics"),
            "balancing_technique": doc.get("balancing_technique"),
            "dimensionality_reduction_method": doc.get("dimensionality_reduction_method"),
            "selected_features_count": doc.get("selected_features_count"),
            "training_timestamp": doc.get("training_timestamp"),
            "evaluation_timestamp": doc.get("evaluation_timestamp"),
            "explainability": doc.get("explainability"),
            "created_at": created_at.isoformat() if isinstance(created_at, datetime) else str(created_at)
        }
