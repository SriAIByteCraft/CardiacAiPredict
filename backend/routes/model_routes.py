"""
Model Metrics and Benchmark Routes Blueprint.
GET /api/model/metrics
GET /api/model/comparison
"""
from flask import Blueprint, send_file
import os
from ..services.model_service import ModelService
from ..utils.responses import success_response, error_response

model_bp = Blueprint("model", __name__)

@model_bp.route("/metrics", methods=["GET"])
def get_metrics():
    res = ModelService.get_metrics()
    if not res.get("success"):
        return error_response(
            message=res.get("message"),
            error_code=res.get("code", "METRICS_UNAVAILABLE"),
            status_code=res.get("status", 503)
        )
    return success_response(data=res.get("data"), status_code=200)

@model_bp.route("/comparison", methods=["GET"])
def get_comparison():
    res = ModelService.get_comparison()
    if not res.get("success"):
        return error_response(
            message=res.get("message"),
            error_code=res.get("code", "COMPARISON_UNAVAILABLE"),
            status_code=res.get("status", 503)
        )
    return success_response(data=res.get("data"), status_code=200)
