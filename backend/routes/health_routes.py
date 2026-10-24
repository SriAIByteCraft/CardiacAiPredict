"""
Health and Diagnostic Check Routes.
GET /api/health
GET /api/database-health
"""
from flask import Blueprint
from ..services.model_service import ModelService
from ..utils.responses import success_response, error_response

health_bp = Blueprint("health", __name__)

@health_bp.route("/health", methods=["GET"])
def health():
    res = ModelService.get_health()
    return success_response(data=res.get("data"), message="Service is operational.")

@health_bp.route("/database-health", methods=["GET"])
def db_health():
    res = ModelService.get_database_health()
    if not res.get("success"):
        return error_response(
            message="Database connection degraded or disconnected.",
            details=res.get("data"),
            status_code=503
        )
    return success_response(data=res.get("data"), message="Database connected and operational.")
