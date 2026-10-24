"""
User Profile and Account Management Service.
Handles profile updates and secure password changes.
"""
from datetime import datetime, timezone
from bson import ObjectId
from ..database.mongodb import get_db
from ..models.user import User
from ..utils.validators import validate_password_change

class UserService:

    @staticmethod
    def get_profile(user_dict: dict):
        return {
            "success": True,
            "data": {"user": User.to_safe_dict(user_dict)},
            "status": 200
        }

    @staticmethod
    def update_profile(user_dict: dict, payload: dict):
        if not isinstance(payload, dict):
            return {"success": False, "message": "Invalid request format.", "status": 400}

        name = payload.get("name", "").strip()
        if not name or len(name) < 2:
            return {"success": False, "message": "Name must be at least 2 characters long.", "status": 400}

        db = get_db()
        user_id = user_dict["_id"]
        now = datetime.now(timezone.utc)

        db.users.update_one(
            {"_id": user_id},
            {"$set": {"name": name, "updated_at": now}}
        )

        user_dict["name"] = name
        user_dict["updated_at"] = now

        return {
            "success": True,
            "message": "Profile updated successfully.",
            "data": {"user": User.to_safe_dict(user_dict)},
            "status": 200
        }

    @staticmethod
    def change_password(user_dict: dict, payload: dict):
        is_valid, msg, val_data = validate_password_change(payload)
        if not is_valid:
            return {"success": False, "message": msg, "status": 400}

        current_pw = val_data["current_password"]
        new_pw = val_data["new_password"]

        if not User.verify_password(user_dict.get("password_hash", ""), current_pw):
            return {
                "success": False,
                "message": "Current password is incorrect.",
                "code": "INVALID_CURRENT_PASSWORD",
                "status": 400
            }

        db = get_db()
        user_id = user_dict["_id"]
        now = datetime.now(timezone.utc)

        new_hash = User.hash_password(new_pw)
        db.users.update_one(
            {"_id": user_id},
            {"$set": {"password_hash": new_hash, "updated_at": now}}
        )

        return {
            "success": True,
            "message": "Password changed successfully.",
            "status": 200
        }
