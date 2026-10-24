"""
Profile Management Routes Blueprint.
"""
from flask import Blueprint, request, g
from ..middleware.auth_middleware import login_required
from ..services.user_service import UserService
from ..utils.responses import success_response, error_response

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("", methods=["GET"])
@login_required
def get_profile():
    res = UserService.get_profile(g.current_user)
    return success_response(data=res.get("data"), status_code=200)

@profile_bp.route("", methods=["PATCH", "PUT"])
@login_required
def update_profile():
    payload = request.get_json(silent=True) or {}
    res = UserService.update_profile(g.current_user, payload)
    if not res.get("success"):
        return error_response(message=res.get("message"), status_code=res.get("status", 400))
    return success_response(data=res.get("data"), message=res.get("message"), status_code=200)

@profile_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    payload = request.get_json(silent=True) or {}
    res = UserService.change_password(g.current_user, payload)
    if not res.get("success"):
        return error_response(
            message=res.get("message"),
            error_code=res.get("code", "PASSWORD_CHANGE_FAILED"),
            status_code=res.get("status", 400)
        )
    return success_response(message=res.get("message"), status_code=200)
