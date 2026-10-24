"""
User Document Model and Security Helper.
Handles password hashing via Werkzeug, email normalization, and safe serialization.
"""
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

class User:
    """Represents an application user."""

    @staticmethod
    def normalize_email(email: str) -> str:
        """Converts email to lowercase and strips leading/trailing whitespace."""
        return str(email).strip().lower() if email else ""

    @staticmethod
    def hash_password(password: str) -> str:
        """Generates secure scrypt or pbkdf2 password hash."""
        return generate_password_hash(password)

    @staticmethod
    def verify_password(stored_hash: str, candidate_password: str) -> bool:
        """Compares plain password against stored Werkzeug hash."""
        if not stored_hash or not candidate_password:
            return False
        return check_password_hash(stored_hash, candidate_password)

    @staticmethod
    def create_document(name: str, email: str, password: str) -> dict:
        """Creates a sanitized MongoDB user document."""
        now = datetime.now(timezone.utc)
        return {
            "name": name.strip(),
            "email": User.normalize_email(email),
            "password_hash": User.hash_password(password),
            "created_at": now,
            "updated_at": now
        }

    @staticmethod
    def to_safe_dict(user_doc: dict) -> dict:
        """
        Serializes user document omitting sensitive password hash.
        Converts ObjectId and datetimes to ISO strings.
        """
        if not user_doc:
            return {}
        
        user_id = str(user_doc["_id"]) if "_id" in user_doc else None
        created_at = user_doc.get("created_at")
        updated_at = user_doc.get("updated_at")

        return {
            "id": user_id,
            "name": user_doc.get("name", ""),
            "email": user_doc.get("email", ""),
            "created_at": created_at.isoformat() if isinstance(created_at, datetime) else str(created_at),
            "updated_at": updated_at.isoformat() if isinstance(updated_at, datetime) else str(updated_at)
        }
