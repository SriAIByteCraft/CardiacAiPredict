"""
Tests for Authentication Endpoints (Registration, Login, Logout, Session Verification).
"""
import pytest

def test_register_success(client):
    payload = {
        "name": "Alice Smith",
        "email": "alice.smith@hospital.org",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 201
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["user"]["email"] == "alice.smith@hospital.org"
    assert "password_hash" not in data["data"]["user"]

def test_register_duplicate_email(client):
    payload = {
        "name": "Alice Smith",
        "email": "alice.duplicate@hospital.org",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    first_res = client.post("/api/auth/register", json=payload)
    assert first_res.status_code == 201
    
    dup_res = client.post("/api/auth/register", json=payload)
    assert dup_res.status_code == 409
    dup_data = dup_res.get_json()
    assert dup_data["success"] is False
    assert dup_data["error_code"] == "DUPLICATE_EMAIL"

def test_register_weak_password(client):
    payload = {
        "name": "Weak User",
        "email": "weak@example.com",
        "password": "123",
        "confirm_password": "123"
    }
    res = client.post("/api/auth/register", json=payload)
    assert res.status_code == 400
    assert res.get_json()["success"] is False

def test_login_success(client):
    # Register user first
    client.post("/api/auth/register", json={
        "name": "Bob Vance",
        "email": "bob@refrigeration.com",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })

    # Login
    res = client.post("/api/auth/login", json={
        "email": "bob@refrigeration.com",
        "password": "Password123!"
    })
    assert res.status_code == 200
    data = res.get_json()
    assert data["success"] is True
    assert data["data"]["user"]["name"] == "Bob Vance"

def test_login_invalid_password(client):
    client.post("/api/auth/register", json={
        "name": "Charlie",
        "email": "charlie@hospital.org",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })

    res = client.post("/api/auth/login", json={
        "email": "charlie@hospital.org",
        "password": "WrongPassword!"
    })
    assert res.status_code == 401
    assert res.get_json()["success"] is False

def test_unauthenticated_me(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401
    assert res.get_json()["error_code"] == "UNAUTHORIZED"

def test_logout(auth_client):
    res = auth_client.post("/api/auth/logout")
    assert res.status_code == 200
    assert res.get_json()["success"] is True

    # Verify session cleared
    me_res = auth_client.get("/api/auth/me")
    assert me_res.status_code == 401
