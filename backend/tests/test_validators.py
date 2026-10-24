"""
Tests for Validators and Model Services.
"""
try:
    from backend.utils.validators import is_valid_email, is_strong_password, validate_registration
    from backend.services.model_service import ModelService
except ImportError:
    from utils.validators import is_valid_email, is_strong_password, validate_registration
    from services.model_service import ModelService

def test_email_validation():
    assert is_valid_email("patient@domain.com") is True
    assert is_valid_email("invalid-email") is False
    assert is_valid_email("") is False

def test_password_strength():
    valid, _ = is_strong_password("ValidPassword123")
    assert valid is True

    short, msg = is_strong_password("Ab1")
    assert short is False

    no_digit, _ = is_strong_password("NoDigitsHereAtAll")
    assert no_digit is False

def test_health_endpoint(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json()["data"]["status"] == "online"

def test_database_health_endpoint(client):
    res = client.get("/api/database-health")
    assert res.status_code == 200
    assert res.get_json()["data"]["connected"] is True
