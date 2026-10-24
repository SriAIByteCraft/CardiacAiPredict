"""
Authentication Routes Blueprint.
Handles registration, login, logout, and current user retrieval.
"""
try:
    from ..services.auth_service import AuthService
    from ..middleware.auth_middleware import login_required, get_current_user
    from ..middleware.rate_limiter import auth_rate_limiter
    from ..models.user import User
    from ..utils.responses import success_response, error_response
except (ImportError, ValueError):
    from services.auth_service import AuthService
    from middleware.auth_middleware import login_required, get_current_user
    from middleware.rate_limiter import auth_rate_limiter
    from models.user import User
    from utils.responses import success_response, error_response

from flask import Blueprint, request

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
@auth_rate_limiter.limit()
def register():
    payload = request.get_json(silent=True) or {}
    res = AuthService.register(payload)
    if not res.get("success"):
        return error_response(
            message=res.get("message"),
            error_code=res.get("code", "REGISTRATION_FAILED"),
            status_code=res.get("status", 400)
        )
    return success_response(
        data=res.get("data"),
        message=res.get("message"),
        status_code=201
    )

@auth_bp.route("/login", methods=["POST"])
@auth_rate_limiter.limit()
def login():
    payload = request.get_json(silent=True) or {}
    res = AuthService.login(payload)
    if not res.get("success"):
        return error_response(
            message=res.get("message"),
            error_code=res.get("code", "LOGIN_FAILED"),
            status_code=res.get("status", 401)
        )
    return success_response(
        data=res.get("data"),
        message=res.get("message"),
        status_code=200
    )

@auth_bp.route("/logout", methods=["POST"])
def logout():
    res = AuthService.logout()
    return success_response(message=res.get("message"), status_code=200)

@auth_bp.route("/me", methods=["GET"])
@login_required
def get_me():
    user = get_current_user()
    return success_response(
        data={"user": User.to_safe_dict(user)},
        message="Authenticated session valid."
    )
