"""
Model Service.
Provides verified model performance metrics, comparative experiment benchmarks,
and diagnostic health information.
"""
import os
import json
from flask import current_app
from ..database.mongodb import check_connection
from ..ml.predict_model import get_predictor

class ModelService:

    @staticmethod
    def _get_metrics_file_path():
        if current_app:
            return current_app.config.get("METRICS_ARTIFACT_PATH")
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(base_dir, "ml", "artifacts", "model_metrics.json")

    @staticmethod
    def _get_comparison_file_path():
        if current_app:
            return current_app.config.get("COMPARISON_ARTIFACT_PATH")
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        return os.path.join(base_dir, "ml", "artifacts", "model_comparison.json")

    @staticmethod
    def get_metrics():
        metrics_path = ModelService._get_metrics_file_path()
        if not os.path.exists(metrics_path):
            return {
                "success": False,
                "message": "Model evaluation metrics not yet generated. Please execute `python scripts/train_model.py`.",
                "code": "METRICS_NOT_FOUND",
                "status": 503
            }

        try:
            with open(metrics_path, "r") as f:
                data = json.load(f)
            return {"success": True, "data": data, "status": 200}
        except Exception as e:
            return {"success": False, "message": f"Failed to read metrics artifact: {e}", "status": 500}

    @staticmethod
    def get_comparison():
        comp_path = ModelService._get_comparison_file_path()
        if not os.path.exists(comp_path):
            return {
                "success": False,
                "message": "Model comparison benchmarks not yet generated. Please execute `python scripts/train_model.py`.",
                "code": "COMPARISON_NOT_FOUND",
                "status": 503
            }

        try:
            with open(comp_path, "r") as f:
                data = json.load(f)
            return {"success": True, "data": data, "status": 200}
        except Exception as e:
            return {"success": False, "message": f"Failed to read comparison artifact: {e}", "status": 500}

    @staticmethod
    def get_health():
        predictor = get_predictor()
        db_status = check_connection()
        
        return {
            "success": True,
            "data": {
                "service": "Heart Disease Prediction System API",
                "status": "online",
                "model_loaded": predictor.is_loaded,
                "model_version": predictor.metadata.get("version", "1.0.0") if predictor.is_loaded else None,
                "database": db_status
            },
            "status": 200
        }

    @staticmethod
    def get_database_health():
        db_status = check_connection()
        return {
            "success": db_status.get("connected", False),
            "data": db_status,
            "status": 200 if db_status.get("connected") else 503
        }
