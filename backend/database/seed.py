"""
Database Seeder for Demo Accounts and Sample Clinical Assessments.
Ensures a demo user and sample assessments exist so reviewers/users can immediately
test and explore the application without manual setup.
"""
import logging
from datetime import datetime, timedelta, timezone
from bson import ObjectId

logger = logging.getLogger(__name__)

DEMO_USER_EMAIL = "demo@cardiopredict.com"
DEMO_USER_PASSWORD = "DemoUser2026!"
DEMO_USER_NAME = "Dr. Demo Clinician"

def seed_demo_data(db):
    """
    Seeds a demo clinician account and realistic sample clinical predictions
    into the database if they do not already exist.
    """
    if db is None:
        return

    try:
        from ..models.user import User
    except (ImportError, ValueError):
        from models.user import User

    # 1. Seed or retrieve Demo User
    user = db.users.find_one({"email": DEMO_USER_EMAIL})
    if not user:
        user_doc = User.create_document(
            name=DEMO_USER_NAME,
            email=DEMO_USER_EMAIL,
            password=DEMO_USER_PASSWORD
        )
        insert_res = db.users.insert_one(user_doc)
        user_id = str(insert_res.inserted_id)
        logger.info(f"[Database Seed] Created demo user '{DEMO_USER_EMAIL}' with ID {user_id}")
    else:
        user_id = str(user["_id"])
        # Ensure password hash is fresh and valid
        db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"password_hash": User.hash_password(DEMO_USER_PASSWORD)}}
        )
        logger.info(f"[Database Seed] Demo user '{DEMO_USER_EMAIL}' exists (ID: {user_id})")

    # 2. Check if sample predictions exist for this user
    existing_preds = db.predictions.count_documents({"user_id": user_id})
    if existing_preds == 0:
        logger.info("[Database Seed] Seeding sample clinical assessments for demo user...")
        now = datetime.now(timezone.utc)

        sample_cases = [
            {
                "offset_days": 4,
                "patient_name": "Eleanor Vance",
                "patient_phone": "+1 (555) 234-5678",
                "patient_address": "742 Evergreen Terrace, Springfield",
                "prediction": 0,
                "prediction_label": "No Heart Disease Detected",
                "probability": 0.124,
                "probability_breakdown": {"disease_negative": 0.876, "disease_positive": 0.124},
                "risk_level": "Low Risk",
                "features": {
                    "age": 45, "sex": 1, "cp": 2, "trestbps": 120, "chol": 195,
                    "fbs": 0, "restecg": 0, "thalach": 168, "exang": 0,
                    "oldpeak": 0.0, "slope": 1, "ca": 0, "thal": 3
                }
            },
            {
                "offset_days": 3,
                "patient_name": "Arthur Pendelton",
                "patient_phone": "+1 (555) 876-5432",
                "patient_address": "1204 Oak Ridge Lane, Seattle, WA",
                "prediction": 1,
                "prediction_label": "Heart Disease Indicated",
                "probability": 0.842,
                "probability_breakdown": {"disease_negative": 0.158, "disease_positive": 0.842},
                "risk_level": "High Risk",
                "features": {
                    "age": 62, "sex": 1, "cp": 4, "trestbps": 145, "chol": 282,
                    "fbs": 1, "restecg": 2, "thalach": 122, "exang": 1,
                    "oldpeak": 2.4, "slope": 2, "ca": 2, "thal": 7
                }
            },
            {
                "offset_days": 2,
                "patient_name": "Maria Rodriguez",
                "patient_phone": "+1 (555) 432-1098",
                "patient_address": "88 Palm Canyon Dr, Phoenix, AZ",
                "prediction": 0,
                "prediction_label": "No Heart Disease Detected",
                "probability": 0.285,
                "probability_breakdown": {"disease_negative": 0.715, "disease_positive": 0.285},
                "risk_level": "Moderate Risk",
                "features": {
                    "age": 52, "sex": 0, "cp": 3, "trestbps": 132, "chol": 215,
                    "fbs": 0, "restecg": 1, "thalach": 154, "exang": 0,
                    "oldpeak": 0.8, "slope": 1, "ca": 0, "thal": 3
                }
            },
            {
                "offset_days": 1,
                "patient_name": "Jonathan Hayes",
                "patient_phone": "+1 (555) 901-2345",
                "patient_address": "450 Lexington Ave, New York, NY",
                "prediction": 1,
                "prediction_label": "Heart Disease Indicated",
                "probability": 0.912,
                "probability_breakdown": {"disease_negative": 0.088, "disease_positive": 0.912},
                "risk_level": "High Risk",
                "features": {
                    "age": 67, "sex": 1, "cp": 4, "trestbps": 160, "chol": 298,
                    "fbs": 0, "restecg": 2, "thalach": 108, "exang": 1,
                    "oldpeak": 3.2, "slope": 2, "ca": 3, "thal": 7
                }
            },
            {
                "offset_days": 0,
                "patient_name": "Chloe Bennett",
                "patient_phone": "+1 (555) 345-6789",
                "patient_address": "310 Sunset Blvd, Los Angeles, CA",
                "prediction": 0,
                "prediction_label": "No Heart Disease Detected",
                "probability": 0.089,
                "probability_breakdown": {"disease_negative": 0.911, "disease_positive": 0.089},
                "risk_level": "Low Risk",
                "features": {
                    "age": 41, "sex": 0, "cp": 1, "trestbps": 110, "chol": 172,
                    "fbs": 0, "restecg": 0, "thalach": 175, "exang": 0,
                    "oldpeak": 0.0, "slope": 1, "ca": 0, "thal": 3
                }
            }
        ]

        docs_to_insert = []
        for case in sample_cases:
            created_time = now - timedelta(days=case["offset_days"], hours=2)
            docs_to_insert.append({
                "user_id": user_id,
                "patient_name": case.get("patient_name", "Unnamed Patient"),
                "patient_phone": case.get("patient_phone", ""),
                "patient_address": case.get("patient_address", ""),
                "validated_features": case["features"],
                "prediction": case["prediction"],
                "prediction_label": case["prediction_label"],
                "probability": case["probability"],
                "probability_breakdown": case["probability_breakdown"],
                "risk_level": case["risk_level"],
                "model_version": "1.0.0",
                "created_at": created_time
            })

        db.predictions.insert_many(docs_to_insert)
        logger.info(f"[Database Seed] Inserted {len(docs_to_insert)} sample assessments.")
