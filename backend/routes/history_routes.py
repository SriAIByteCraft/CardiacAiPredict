"""
Prediction History Routes Blueprint.
GET /api/history
GET /api/history/<prediction_id>
DELETE /api/history/<prediction_id>
"""
from flask import Blueprint, request, g
from ..middleware.auth_middleware import login_required
from ..services.history_service import HistoryService
from ..utils.responses import success_response, error_response

history_bp = Blueprint("history", __name__)

@history_bp.route("", methods=["GET"])
@login_required
def get_history():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    risk_filter = request.args.get("risk", None, type=str)
    
    user_id = str(g.current_user["_id"])
    res = HistoryService.get_user_history(user_id, page=page, per_page=per_page, risk_filter=risk_filter)
    return success_response(data=res.get("data"), status_code=200)

@history_bp.route("/<prediction_id>", methods=["GET"])
@login_required
def get_prediction_detail(prediction_id):
    user_id = str(g.current_user["_id"])
    res = HistoryService.get_prediction_by_id(user_id, prediction_id)
    if not res.get("success"):
        return error_response(
            message=res.get("message"),
            error_code=res.get("code", "NOT_FOUND"),
            status_code=res.get("status", 404)
        )
    return success_response(data=res.get("data"), status_code=200)

@history_bp.route("/<prediction_id>", methods=["DELETE"])
@login_required
def delete_prediction(prediction_id):
    user_id = str(g.current_user["_id"])
    res = HistoryService.delete_prediction(user_id, prediction_id)
    if not res.get("success"):
        return error_response(message=res.get("message"), status_code=res.get("status", 400))
    return success_response(message=res.get("message"), status_code=200)
