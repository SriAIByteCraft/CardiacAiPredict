"""
Authentication Service.
Handles registration with duplicate email detection, credential validation,
and secure session management.
"""
from flask import session
from ..database.mongodb import get_db
from ..models.user import User
from ..utils.validators import validate_registration, validate_login

class AuthService:
    
    @staticmethod
    def register(data: dict):
        is_valid, msg, validated_data = validate_registration(data)
        if not is_valid:
            return {"success": False, "message": msg, "code": "VALIDATION_ERROR", "status": 400}

        db = get_db()
        email = validated_data["email"]

        # Check for duplicate email
        existing_user = db.users.find_one({"email": email})
        if existing_user:
            return {
                "success": False,
                "message": "An account with this email address already exists.",
                "code": "DUPLICATE_EMAIL",
                "status": 409
            }

        # Create user document
        user_doc = User.create_document(
            name=validated_data["name"],
            email=email,
            password=validated_data["password"]
        )

        insert_result = db.users.insert_one(user_doc)
        user_doc["_id"] = insert_result.inserted_id

        # Set session on registration
        session["user_id"] = str(insert_result.inserted_id)
        session.permanent = True

        return {
            "success": True,
            "message": "Registration successful. Welcome!",
            "data": {"user": User.to_safe_dict(user_doc)},
            "status": 201
        }

    @staticmethod
    def login(data: dict):
        is_valid, msg, validated_data = validate_login(data)
        if not is_valid:
            return {"success": False, "message": msg, "code": "VALIDATION_ERROR", "status": 400}

        db = get_db()
        email = validated_data["email"]
        user = db.users.find_one({"email": email})

        if not user or not User.verify_password(user.get("password_hash", ""), validated_data["password"]):
            return {
                "success": False,
                "message": "Invalid email or password credentials.",
                "code": "INVALID_CREDENTIALS",
                "status": 401
            }

        # Set session
        session["user_id"] = str(user["_id"])
        session.permanent = True

        return {
            "success": True,
            "message": "Login successful.",
            "data": {"user": User.to_safe_dict(user)},
            "status": 200
        }

    @staticmethod
    def logout():
        session.clear()
        return {"success": True, "message": "Successfully logged out.", "status": 200}
