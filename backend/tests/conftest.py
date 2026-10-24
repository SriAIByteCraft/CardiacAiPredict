"""
Pytest Fixtures for Full-Stack Flask Backend Testing.
Configures test app with mongomock in-memory database and provides authenticated clients.
"""
import pytest
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from backend.app import create_app
    from backend.database.mongodb import get_db
except ImportError:
    from app import create_app
    from database.mongodb import get_db

@pytest.fixture
def app():
    """Creates Flask application instance under testing configuration."""
    app_instance = create_app("testing")
    app_instance.config["TESTING"] = True
    app_instance.config["WTF_CSRF_ENABLED"] = False
    
    with app_instance.app_context():
        # Clear mock database collections before test
        db = get_db()
        db.users.delete_many({})
        db.predictions.delete_many({})
        db.model_metrics.delete_many({})
        yield app_instance

@pytest.fixture
def client(app):
    """Test client for unauthenticated HTTP requests."""
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """
    Test client pre-authenticated with a registered test user.
    """
    reg_payload = {
        "name": "Dr. Sarah Jenkins",
        "email": "sarah.jenkins@hospital.org",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }
    resp = client.post("/api/auth/register", json=reg_payload)
    assert resp.status_code == 201
    return client

@pytest.fixture
def sample_prediction_payload():
    """Valid patient medical attributes matching UCI Cleveland schema."""
    return {
        "age": 55,
        "sex": 1,
        "cp": 4,
        "trestbps": 140,
        "chol": 242,
        "fbs": 0,
        "restecg": 0,
        "thalach": 128,
        "exang": 1,
        "oldpeak": 1.4,
        "slope": 2,
        "ca": 1,
        "thal": 7
    }
