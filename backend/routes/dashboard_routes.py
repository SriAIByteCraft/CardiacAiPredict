"""
Dashboard Routes Blueprint.
GET /api/dashboard/stats
GET /api/dashboard/recent
"""
from flask import Blueprint, g
from ..middleware.auth_middleware import login_required
from ..services.dashboard_service import DashboardService
from ..utils.responses import success_response

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/stats", methods=["GET"])
@login_required
def get_stats():
    user_id = str(g.current_user["_id"])
    res = DashboardService.get_dashboard_stats(user_id)
    return success_response(data=res.get("data"), status_code=200)

@dashboard_bp.route("/recent", methods=["GET"])
@login_required
def get_recent():
    user_id = str(g.current_user["_id"])
    res = DashboardService.get_recent_predictions(user_id)
    return success_response(data=res.get("data"), status_code=200)
