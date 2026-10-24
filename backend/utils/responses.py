"""
Consistent API JSON Response Utilities.
Ensures uniform payload shapes across all API endpoints.
"""
from flask import jsonify

def success_response(data=None, message="Operation successful", status_code=200):
    """Formats standardized success response."""
    payload = {
        "success": True,
        "message": message,
        "data": data if data is not None else {}
    }
    return jsonify(payload), status_code

def error_response(message="An error occurred", error_code="BAD_REQUEST", details=None, status_code=400):
    """Formats standardized error response."""
    payload = {
        "success": False,
        "message": message,
        "error_code": error_code
    }
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status_code
