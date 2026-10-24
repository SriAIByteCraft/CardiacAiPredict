# MongoDB Atlas Database Schema Documentation

Database Name: `heart_disease_db`

The database consists of three collections: `users`, `predictions`, and `model_metrics`.

---

## 1. `users` Collection

Stores clinician and research user accounts. Passwords are encrypted using Werkzeug's secure hashing algorithm (scrypt/pbkdf2). Plain-text passwords are never stored.

### Document Schema:
```json
{
  "_id": "ObjectId('6719273a0e91c784...')",
  "name": "Dr. Sarah Jenkins",
  "email": "sarah.jenkins@hospital.org",
  "password_hash": "scrypt:32768:8:1$K7pX...$9a8f...",
  "created_at": "ISODate('2026-10-23T14:15:30.000Z')",
  "updated_at": "ISODate('2026-10-23T14:15:30.000Z')"
}
```

### Indexes:
1. `{"email": 1}` — **Unique index**. Guarantees duplicate email registrations are rejected at the database engine level.
2. `{"created_at": -1}` — Standard descending index for administrative audits.

---

## 2. `predictions` Collection

Stores every patient cardiovascular risk evaluation performed by authenticated users. Queries are strictly scoped to the authenticated `user_id`.

### Document Schema:
```json
{
  "_id": "ObjectId('6719274c0e91c784...')",
  "user_id": "6719273a0e91c784...",
  "validated_features": {
    "age": 58,
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
  },
  "prediction": 1,
  "prediction_label": "Presence of Heart Disease Indicator",
  "probability": 0.8842,
  "probability_breakdown": {
    "no_disease": 0.1158,
    "disease": 0.8842
  },
  "risk_level": "Elevated Risk",
  "model_version": "1.0.0",
  "created_at": "ISODate('2026-10-23T14:20:10.000Z')"
}
```

### Indexes:
1. `{"user_id": 1, "created_at": -1}` — **Compound index**. Ensures $O(\log n)$ performance for paginated user history queries.
2. `{"created_at": -1}` — For chronological dashboard rollups.

---

## 3. `model_metrics` Collection

Stores snapshot provenance of trained model runs, dataset metadata, and benchmark results.

### Document Schema:
```json
{
  "_id": "ObjectId('6719275d0e91c784...')",
  "model_version": "1.0.0",
  "model_name": "StackingClassifier (LR + RF + SVM -> Meta LR)",
  "dataset_info": "UCI Cleveland Heart Disease",
  "sample_counts": {
    "total": 303,
    "train": 242,
    "test": 61,
    "disease_positive": 139,
    "disease_negative": 164
  },
  "evaluation_metrics": {
    "accuracy": 0.8852,
    "precision": 0.8387,
    "recall": 0.9286,
    "specificity": 0.8485,
    "f1_score": 0.8814,
    "roc_auc": 0.9600,
    "confusion_matrix": {
      "matrix": [[28, 5], [2, 26]],
      "true_negatives": 28,
      "false_positives": 5,
      "false_negatives": 2,
      "true_positives": 26
    }
  },
  "balancing_technique": "Baseline (None) & SMOTE comparative evaluation",
  "dimensionality_reduction_method": "Full features baseline & PCA / SelectKBest comparison",
  "selected_features_count": 13,
  "training_timestamp": "2026-10-23T14:28:10.000Z",
  "evaluation_timestamp": "2026-10-23T14:28:12.000Z"
}
```

### Indexes:
1. `{"model_version": 1}` — Quick lookup of specific versioned metadata.
