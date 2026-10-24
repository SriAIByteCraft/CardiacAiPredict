"""
Tests for Prediction History and Dashboard Analytics Endpoints.
Verifies user-scoped isolation, pagination, and statistics.
"""
import pytest
try:
    from backend.database.mongodb import get_db
    from backend.models.prediction import Prediction
except ImportError:
    from database.mongodb import get_db
    from models.prediction import Prediction

def test_history_unauthenticated(client):
    res = client.get("/api/history")
    assert res.status_code == 401

def test_history_empty_state(auth_client):
    res = auth_client.get("/api/history")
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert data["items"] == []
    assert data["pagination"]["total_count"] == 0

def test_history_user_isolation(client):
    # Register User A
    client.post("/api/auth/register", json={
        "name": "User A",
        "email": "userA@hospital.org",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    me_a = client.get("/api/auth/me").get_json()["data"]["user"]
    user_a_id = me_a["id"]

    # Insert a prediction record for User A
    db = get_db()
    pred_doc = Prediction.create_document(
        user_id=user_a_id,
        validated_features={"age": 60},
        prediction_result={
            "prediction": 1,
            "prediction_label": "Presence of Heart Disease Indicator",
            "probability": 0.85,
            "risk_level": "Elevated Risk",
            "model_version": "1.0.0"
        }
    )
    insert_res = db.predictions.insert_one(pred_doc)
    doc_id = str(insert_res.inserted_id)

    # User A can retrieve it
    history_a = client.get("/api/history").get_json()["data"]["items"]
    assert len(history_a) == 1
    assert history_a[0]["id"] == doc_id

    # Register User B
    client.post("/api/auth/logout")
    client.post("/api/auth/register", json={
        "name": "User B",
        "email": "userB@hospital.org",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })

    # User B history should be empty (strict user isolation)
    history_b = client.get("/api/history").get_json()["data"]["items"]
    assert len(history_b) == 0

    # User B cannot access User A's prediction by direct ID
    detail_res = client.get(f"/api/history/{doc_id}")
    assert detail_res.status_code == 404

def test_dashboard_stats(auth_client):
    res = auth_client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.get_json()["data"]
    assert "total_predictions" in data
    assert "activity_timeline" in data
