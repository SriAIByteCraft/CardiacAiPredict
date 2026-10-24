"""
Prediction History Service.
Strictly scopes all queries to the authenticated user's session identifier.
Supports pagination, date sorting, detail lookup, and record deletion.
"""
from bson import ObjectId
from pymongo import DESCENDING
from ..database.mongodb import get_db
from ..models.prediction import Prediction

class HistoryService:

    @staticmethod
    def get_user_history(user_id: str, page=1, per_page=10, risk_filter=None):
        """
        Retrieves paginated history for the authenticated user only.
        """
        db = get_db()
        query = {"user_id": str(user_id)}
        
        if risk_filter and risk_filter.lower() != "all":
            query["risk_level"] = {"$regex": f"^{risk_filter}", "$options": "i"}

        total_count = db.predictions.count_documents(query)
        
        # Calculate pagination
        page = max(1, int(page))
        per_page = max(1, min(50, int(per_page)))
        skip = (page - 1) * per_page
        total_pages = max(1, (total_count + per_page - 1) // per_page)

        cursor = (
            db.predictions.find(query)
            .sort("created_at", DESCENDING)
            .skip(skip)
            .limit(per_page)
        )

        items = [Prediction.to_safe_dict(doc) for doc in cursor]

        return {
            "success": True,
            "data": {
                "items": items,
                "pagination": {
                    "total_count": total_count,
                    "page": page,
                    "per_page": per_page,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            },
            "status": 200
        }

    @staticmethod
    def get_prediction_by_id(user_id: str, prediction_id: str):
        """
        Retrieves a single prediction record, strictly verifying user ownership.
        """
        if not prediction_id or not ObjectId.is_valid(prediction_id):
            return {"success": False, "message": "Invalid prediction ID format.", "status": 400}

        db = get_db()
        doc = db.predictions.find_one({
            "_id": ObjectId(prediction_id),
            "user_id": str(user_id)
        })

        if not doc:
            return {
                "success": False,
                "message": "Prediction record not found or access denied.",
                "code": "NOT_FOUND",
                "status": 404
            }

        return {
            "success": True,
            "data": {"prediction": Prediction.to_safe_dict(doc)},
            "status": 200
        }

    @staticmethod
    def delete_prediction(user_id: str, prediction_id: str):
        """
        Deletes a user's single prediction record.
        """
        if not prediction_id or not ObjectId.is_valid(prediction_id):
            return {"success": False, "message": "Invalid prediction ID format.", "status": 400}

        db = get_db()
        result = db.predictions.delete_one({
            "_id": ObjectId(prediction_id),
            "user_id": str(user_id)
        })

        if result.deleted_count == 0:
            return {
                "success": False,
                "message": "Record not found or already deleted.",
                "status": 404
            }

        return {
            "success": True,
            "message": "Prediction record deleted successfully.",
            "status": 200
        }
