"""
Authentication Middleware and Session Protection Decorators.
Enforces session authentication and attaches verified user object to request context.
"""
from functools import wraps
from flask import session, request, g
from bson import ObjectId
from ..database.mongodb import get_db
from ..utils.responses import error_response

def get_current_user():
    """Retrieves authenticated user from session ID."""
    user_id = session.get("user_id")
    if not user_id:
        return None

    db = get_db()
    try:
        # Check ObjectId or string ID
        query = {"_id": ObjectId(user_id)} if ObjectId.is_valid(user_id) else {"_id": user_id}
        user = db.users.find_one(query)
        return user
    except Exception:
        return None

def login_required(f):
    """
    Decorator to protect routes requiring an authenticated user.
    Rejects unauthorized requests with 401 status.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return error_response(
                message="Authentication required. Please log in to proceed.",
                error_code="UNAUTHORIZED",
                status_code=401
            )
        g.current_user = user
        return f(*args, **kwargs)
    return decorated_function
