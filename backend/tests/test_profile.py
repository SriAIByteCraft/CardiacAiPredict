"""
Tests for Profile Management and Password Change Endpoints.
"""
import pytest

def test_get_profile(auth_client):
    res = auth_client.get("/api/profile")
    assert res.status_code == 200
    data = res.get_json()["data"]["user"]
    assert data["name"] == "Dr. Sarah Jenkins"
    assert "password_hash" not in data

def test_update_profile(auth_client):
    res = auth_client.patch("/api/profile", json={"name": "Dr. Sarah Jenkins-MD"})
    assert res.status_code == 200
    assert res.get_json()["data"]["user"]["name"] == "Dr. Sarah Jenkins-MD"

def test_change_password_success(auth_client):
    res = auth_client.post("/api/profile/change-password", json={
        "current_password": "Password123!",
        "new_password": "NewSecretPassword456!",
        "confirm_new_password": "NewSecretPassword456!"
    })
    assert res.status_code == 200
    assert res.get_json()["success"] is True

def test_change_password_wrong_current(auth_client):
    res = auth_client.post("/api/profile/change-password", json={
        "current_password": "WrongPassword999!",
        "new_password": "NewSecretPassword456!",
        "confirm_new_password": "NewSecretPassword456!"
    })
    assert res.status_code == 400
    assert res.get_json()["error_code"] == "INVALID_CURRENT_PASSWORD"
