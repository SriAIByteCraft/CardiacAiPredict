"""
Dashboard Analytics Service.
Aggregates summary statistics, recent activity, and timeline data for dashboard charts.
"""
from datetime import datetime, timedelta, timezone
from pymongo import DESCENDING
from ..database.mongodb import get_db
from ..models.prediction import Prediction
from .model_service import ModelService

class DashboardService:

    @staticmethod
    def get_dashboard_stats(user_id: str):
        db = get_db()
        str_user_id = str(user_id)

        # Total predictions by this user
        user_pred_count = db.predictions.count_documents({"user_id": str_user_id})
        
        # Risk breakdown
        elevated_risk_count = db.predictions.count_documents({
            "user_id": str_user_id,
            "prediction": 1
        })
        low_risk_count = db.predictions.count_documents({
            "user_id": str_user_id,
            "prediction": 0
        })

        # Model performance summary
        metrics_res = ModelService.get_metrics()
        model_meta = metrics_res.get("data", {}) if metrics_res.get("success") else {}
        test_metrics = model_meta.get("test_metrics", {})

        # 7-day activity timeline for chart
        now = datetime.now(timezone.utc)
        timeline = []
        for i in range(6, -1, -1):
            day = now - timedelta(days=i)
            day_str = day.strftime("%Y-%m-%d")
            start = datetime(day.year, day.month, day.day, 0, 0, 0, tzinfo=timezone.utc)
            end = start + timedelta(days=1)
            
            day_count = db.predictions.count_documents({
                "user_id": str_user_id,
                "created_at": {"$gte": start, "$lt": end}
            })
            timeline.append({
                "date": day.strftime("%b %d"),
                "count": day_count
            })

        return {
            "success": True,
            "data": {
                "total_predictions": user_pred_count,
                "elevated_risk_count": elevated_risk_count,
                "low_risk_count": low_risk_count,
                "model_accuracy": test_metrics.get("accuracy", "N/A"),
                "model_roc_auc": test_metrics.get("roc_auc", "N/A"),
                "model_f1": test_metrics.get("f1_score", "N/A"),
                "model_version": model_meta.get("version", "1.0.0"),
                "activity_timeline": timeline
            },
            "status": 200
        }

    @staticmethod
    def get_recent_predictions(user_id: str, limit=5):
        db = get_db()
        cursor = (
            db.predictions.find({"user_id": str(user_id)})
            .sort("created_at", DESCENDING)
            .limit(limit)
        )
        recent = [Prediction.to_safe_dict(doc) for doc in cursor]

        return {
            "success": True,
            "data": {"recent_predictions": recent},
            "status": 200
        }
