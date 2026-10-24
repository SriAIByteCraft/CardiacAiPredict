# REST API Documentation

All endpoints return standardized JSON payloads formatted as:
```json
{
  "success": true,
  "message": "Human readable status description",
  "data": { ... }
}
```
Errors return `{"success": false, "message": "...", "error_code": "..."}` with appropriate HTTP status codes (400, 401, 403, 404, 409, 429, 500, 503).

---

## 1. Authentication Endpoints

### `POST /api/auth/register`
Creates a new clinician or user account.
- **Request Body**:
  ```json
  {
    "name": "Dr. Sarah Jenkins",
    "email": "sarah.jenkins@hospital.org",
    "password": "Password123!",
    "confirm_password": "Password123!"
  }
  ```
- **Response (201 Created)**:
  ```json
  {
    "success": true,
    "message": "Registration successful. Welcome!",
    "data": {
      "user": {
        "id": "6719273a0e91c784...",
        "name": "Dr. Sarah Jenkins",
        "email": "sarah.jenkins@hospital.org",
        "created_at": "2026-10-23T14:15:30.000Z"
      }
    }
  }
  ```

### `POST /api/auth/login`
Authenticates user and establishes secure session cookie.
- **Request Body**:
  ```json
  {
    "email": "sarah.jenkins@hospital.org",
    "password": "Password123!"
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Login successful.",
    "data": { "user": { "id": "...", "name": "...", "email": "..." } }
  }
  ```

### `POST /api/auth/logout`
Terminates the session and invalidates cookie.
- **Response (200 OK)**:
  ```json
  { "success": true, "message": "Successfully logged out." }
  ```

### `GET /api/auth/me`
Retrieves current authenticated session user profile. Requires session cookie.
- **Response (200 OK)**:
  ```json
  { "success": true, "data": { "user": { "id": "...", "name": "...", "email": "..." } } }
  ```

---

## 2. Profile Management Endpoints

### `GET /api/profile`
Retrieves user profile.

### `PATCH /api/profile`
Updates user profile fields.
- **Request Body**: `{"name": "Dr. Sarah Jenkins, MD"}`

### `POST /api/profile/change-password`
Modifies user password.
- **Request Body**:
  ```json
  {
    "current_password": "OldPassword123!",
    "new_password": "NewSecretPassword456!",
    "confirm_new_password": "NewSecretPassword456!"
  }
  ```

---

## 3. Prediction Service

### `POST /api/predict`
Executes heart disease risk prediction on 13 patient attributes. Requires authenticated session.
- **Request Body**:
  ```json
  {
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
  }
  ```
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "message": "Prediction generated successfully.",
    "data": {
      "id": "6719274c0e91c784...",
      "prediction": 1,
      "prediction_label": "Presence of Heart Disease Indicator",
      "probability": 0.8842,
      "probability_breakdown": {
        "no_disease": 0.1158,
        "disease": 0.8842
      },
      "confidence": 0.8842,
      "risk_level": "Elevated Risk",
      "risk_badge_class": "risk-high",
      "model_version": "1.0.0",
      "model_architecture": "StackingClassifier",
      "validated_features": { ... },
      "created_at": "2026-10-23T14:20:10.000Z",
      "disclaimer": "This prediction is an educational and research machine learning estimate..."
    }
  }
  ```

---

## 4. History Endpoints

### `GET /api/history`
Retrieves paginated prediction records strictly belonging to the authenticated user.
- **Query Parameters**:
  - `page` (default: 1)
  - `per_page` (default: 10, max: 50)
  - `risk` (optional filter: `all`, `Low`, `Elevated`)
- **Response (200 OK)**:
  ```json
  {
    "success": true,
    "data": {
      "items": [ ... ],
      "pagination": {
        "total_count": 14,
        "page": 1,
        "per_page": 10,
        "total_pages": 2,
        "has_next": true,
        "has_prev": false
      }
    }
  }
  ```

### `GET /api/history/<prediction_id>`
Retrieves single detailed prediction record. Access restricted to owning user.

### `DELETE /api/history/<prediction_id>`
Deletes a prediction record owned by the authenticated user.

---

## 5. Dashboard Endpoints

### `GET /api/dashboard/stats`
Returns user aggregate counts (total, elevated risk, low risk), model test accuracy, and 7-day activity timeline array.

### `GET /api/dashboard/recent`
Returns up to 5 most recent prediction records for the authenticated user.

---

## 6. Model & Health Endpoints

### `GET /api/model/metrics`
Returns verified test metrics, confusion matrix, ROC curve coordinates, and feature importances.

### `GET /api/model/comparison`
Returns cross-validation benchmarks comparing:
- Base classifiers vs Stacking ensemble
- Class balancing techniques (None, SMOTE, Undersampling, Class Weighting)
- Dimensionality reduction techniques (Full Features, PCA, SelectKBest)

### `GET /api/health`
Returns service operational state, model artifact load state, and version.

### `GET /api/database-health`
Returns MongoDB connectivity health diagnostics.
