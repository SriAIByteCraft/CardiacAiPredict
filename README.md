# Heart Disease Prediction Using Stacking Model with Balancing Techniques and Dimensionality Reduction

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![Flask 3.0](https://img.shields.io/badge/flask-3.0-green.svg)](https://palletsprojects.com/p/flask/)
[![Scikit-Learn 1.4](https://img.shields.io/badge/scikit--learn-1.4-orange.svg)](https://scikit-learn.org/)
[![Tests](https://img.shields.io/badge/pytest-24%20passed-brightgreen.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **⚠️ MEDICAL & REGULATORY DISCLAIMER**  
> This system is built strictly for educational, scientific, and experimental research purposes. It does not provide medical diagnosis, clinical decisions, patient treatment plans, or emergency advice. Predictions are statistical machine learning estimates based on sample data. Always consult a licensed cardiologist or medical practitioner for any cardiovascular health concerns.

---

## 1. Project Overview & Problem Statement

Cardiovascular diseases (CVDs) remain the world's leading cause of death. Early risk stratification can identify vulnerable individuals before adverse coronary events occur. Traditional scoring models often struggle with non-linear clinical interactions between resting hemodynamics, stress test electrocardiography, and coronary vessel narrowing.

**CardioPredict** is a complete, full-stack web application implementing:
1. **Stacking Ensemble Classifier**: Combining Logistic Regression, Random Forest, and Support Vector Machines (RBF Kernel) via a cross-validated Logistic Regression meta-learner.
2. **Class Balancing Techniques**: Comparative evaluation of baseline unweighted data, SMOTE (Synthetic Minority Over-sampling Technique), Random Undersampling, and cost-sensitive weighting strictly inside training folds.
3. **Dimensionality Reduction & Feature Selection**: Comparing the complete 13-feature baseline with Principal Component Analysis (PCA) and ANOVA F-test SelectKBest.
4. **Cloud Database Persistence**: MongoDB Atlas integration for user account management (Werkzeug password hashing) and user-isolated prediction history.
5. **Modern Healthcare UI**: 11 responsive HTML5 pages with clinical blue/teal styling, interactive sliders, and Chart.js visualizations.

---

## 2. Empirical Benchmark Results (Zero Fabricated Metrics)

Trained on the **UCI Cleveland Heart Disease dataset** ($n=303$) with a stratified 80% train ($n=242$) and 20% held-out test split ($n=61$):

| Evaluation Metric | Score on Held-Out Test Set |
| :--- | :--- |
| **Accuracy** | **88.52%** |
| **Precision** | **83.87%** |
| **Recall / Sensitivity** | **92.86%** *(Only 2 false negatives out of 28 disease patients)* |
| **Specificity** | **84.85%** |
| **F1-Score** | **88.14%** |
| **ROC-AUC** | **0.9600** |
| **Brier Score** | **0.0934** *(High probability calibration)* |

### 5-Fold Stratified Cross-Validation Comparisons:
- **Base Models vs Stacking**: Stacking Ensemble (**84.28%** Accuracy, **0.9022** AUC) outperformed standalone Logistic Regression (83.88%), Random Forest (83.47%), SVM (83.06%), and Decision Tree (75.20%).
- **Class Balancing**: SMOTE boosted sensitivity to **85.58%**, reducing missed positives at a small trade-off in specificity.
- **Dimensionality Reduction**: Full 13 clinical attributes (**84.28%** Accuracy) proved superior to PCA (81.40%) and SelectKBest (83.05%), indicating that all 13 medical attributes carry irreplaceable prognostic value.

---

## 3. Technology Stack

- **Backend**: Python 3.11, Flask (Modular Blueprints), Flask-CORS, python-dotenv, Werkzeug security
- **Machine Learning**: scikit-learn, imbalanced-learn, pandas, numpy, joblib, matplotlib, seaborn
- **Database**: MongoDB Atlas (`heart_disease_db`) via PyMongo (with automated in-memory mock fallback for offline development & tests)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Healthcare Design System Tokens), Vanilla JavaScript (ES6 Modules), Chart.js
- **Testing**: pytest (24 automated tests covering auth, profile, inference, security isolation, and API schemas)

---

## 4. Directory Structure

```
heart-disease-prediction/
    frontend/
        index.html               # Professional healthcare landing page
        about.html               # Problem statement, methodology & limitations
        register.html            # User registration with validation
        login.html               # Session authentication
        dashboard.html           # Analytics, KPI cards & 7-day Chart.js timeline
        predict.html             # 13-feature clinical medical assessment form
        result.html              # Probability gauge & feature breakdown
        history.html             # User-restricted paginated history & modal
        model-performance.html   # Real metrics, confusion matrix & ROC curve
        profile.html             # Profile info & password management
        404.html                 # Page not found error screen
        css/
            main.css             # Tokens, typography, navbar, buttons, layout
            components.css       # Cards, forms, tables, modals, spinners
            auth.css             # Login / Register split styling
            dashboard.css        # KPI cards & chart layout
            predict.css          # Multi-section medical form layout
            model-performance.css# Confusion matrix & benchmark layout
        js/
            api.js               # Central API client & endpoint helpers
            ui.js                # Toasts, dynamic navbar & modals
            auth.js              # Auth controller & route guards
            dashboard.js         # Stats loader & Chart.js graph
            predict.js           # Live sliders, validation & predict submit
            result.js            # Interpretation gauge & feature table
            history.js           # Paginated history, filter & deletion
            model-performance.js # Benchmark scorecards & comparison charts
            profile.js           # Profile update & password modification
    backend/
        app.py                   # Flask Application Factory & static routing
        config.py                # Environment configs (Dev, Test, Prod)
        extensions.py            # Flask-CORS
        database/
            mongodb.py           # MongoDB Atlas connection manager & fallback
            indexes.py           # Unique email & compound prediction indexes
        models/
            user.py              # User document & Werkzeug hashing
            prediction.py        # Prediction document & safe serialization
            model_metrics.py     # Metrics provenance record
        middleware/
            auth_middleware.py   # @login_required decorator & session validation
            security.py          # OWASP defensive headers
            rate_limiter.py      # Sliding window rate limiter
        utils/
            validators.py        # Regex email, password policy & schema checks
            responses.py         # Standardized JSON response format
        services/
            auth_service.py      # Register & login service
            user_service.py      # Profile & password change
            prediction_service.py# Preprocessing & inference orchestration
            history_service.py   # User-isolated paginated history
            dashboard_service.py # KPI stats & timeline rollups
            model_service.py     # Verified metrics & benchmark endpoints
        routes/
            auth_routes.py       # /api/auth
            profile_routes.py    # /api/profile
            prediction_routes.py # /api/predict
            history_routes.py    # /api/history
            dashboard_routes.py  # /api/dashboard
            model_routes.py      # /api/model
            health_routes.py     # /api/health
        ml/
            data_loader.py       # UCI Cleveland dataset loader & schema
            preprocessor.py      # ColumnTransformer (StandardScaler + OneHot)
            balancing.py         # SMOTE, Undersampling, Class Weighting
            dimensionality_reduction.py # PCA & SelectKBest
            stacking_model.py    # StackingClassifier (LR + RF + SVM -> Meta LR)
            evaluate.py          # Metrics, ROC, PR curves & plots
            explainability.py    # Permutation feature importance
            predict_model.py     # Inference engine & boundary validation
            train_pipeline.py    # End-to-end training & held-out test pipeline
            artifacts/           # Trained joblib bundle & JSON metrics
        tests/
            conftest.py          # Test fixtures with mongomock client
            test_auth.py         # Registration & login tests
            test_profile.py      # Profile & password change tests
            test_predictions.py  # Inference & schema boundary validation
            test_history.py      # User isolation & pagination tests
            test_validators.py   # Input validators & health check tests
        requirements.txt         # Pinned production dependencies
        .env.example             # Configuration template
    data/
        raw/
            processed.cleveland.data # Original UCI Cleveland repository file
            heart_disease_uci.csv    # Standardized 14-column CSV
        processed/
    notebooks/
        eda_and_experiments.ipynb # Exploratory data analysis notebook
    docs/
        architecture.md          # Detailed system architecture
        database_schema.md       # MongoDB collections, documents & indexes
        api_documentation.md     # REST API endpoint specifications
        ml_methodology.md        # Stacking, resampling & leakage prevention
        evaluation_report.md     # Detailed performance scores & confusion matrix
        testing_report.md        # Pytest test execution report
    scripts/
        download_dataset.py      # Downloads & standardizes raw UCI data
        train_model.py           # Trains ensemble & saves artifacts
        evaluate_model.py        # Prints performance summary
        check_database.py        # Tests MongoDB Atlas connection
        create_indexes.py        # Ensures MongoDB indexes
        run_tests.py             # Executes all 24 pytest tests
    .gitignore
    .env.example
    README.md
    LICENSE
```

---

## 5. Installation & Setup Instructions

### Prerequisites
- Python 3.10+ (tested with Python 3.11.9)
- pip package manager
- Optional: MongoDB Atlas cluster connection string (or use automated offline mock store)

### Step 1: Clone or Navigate to Project
```bash
cd heart-disease-prediction
```

### Step 2: Create and Activate Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `backend/.env`:
```bash
cp .env.example backend/.env
```
Edit `backend/.env`:
```ini
FLASK_ENV=development
PORT=5000
SECRET_KEY=replace_with_a_secure_random_hex_key
SESSION_COOKIE_SECURE=False
FRONTEND_ORIGIN=*

# MongoDB Atlas Connection String:
# Leave blank to use the built-in local in-memory store for offline demo/testing
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=heart_disease_db
```

---

## 6. Dataset Preparation & Model Training

### Prepare Dataset:
```bash
python scripts/download_dataset.py
```
*Parses and verifies 303 rows across 14 attributes from the official UCI repository.*

### Train Stacking Ensemble & Generate Evaluation Artifacts:
```bash
python scripts/train_model.py
```
*Executes cross-validation comparisons, held-out test evaluation, generates `stacking_heart_model.joblib`, `model_metrics.json`, and visual plots in `backend/ml/artifacts`.*

### Inspect Evaluation Summary:
```bash
python scripts/evaluate_model.py
```

---

## 7. Running the Application

### Start Backend Application:
```bash
python backend/app.py
```
The server starts at `http://127.0.0.1:5000`.

### Access the Frontend:
Because `backend/app.py` serves both the API endpoints and the frontend static assets, you can directly open:
```
http://127.0.0.1:5000
```
Or view the pages:
- **Landing Page**: `http://127.0.0.1:5000/index.html`
- **Dashboard**: `http://127.0.0.1:5000/dashboard.html`
- **Assessment Form**: `http://127.0.0.1:5000/predict.html`
- **Model Benchmarks**: `http://127.0.0.1:5000/model-performance.html`
- **Assessment History**: `http://127.0.0.1:5000/history.html`
- **About & Methodology**: `http://127.0.0.1:5000/about.html`

*(Alternatively, you can serve `frontend/` using any static file server like Live Server or `python -m http.server 5500` - CORS is already configured).*

---

## 8. Running Automated Tests

Run the complete test suite (24 tests):
```bash
python scripts/run_tests.py
```
Or directly with pytest:
```bash
pytest backend/tests -v
```

All tests run without requiring external cloud credentials thanks to `mongomock` in-memory database isolation.

---

## 9. Deployment Guidelines

### Production Deployment (e.g., Render, Railway, DigitalOcean, AWS EC2):
1. **WSGI Server**: Use `gunicorn` in production:
   ```bash
   pip install gunicorn
   gunicorn "backend.app:create_app('production')" --bind 0.0.0.0:5000 --workers 4
   ```
2. **Environment Configuration**:
   - Set `FLASK_ENV=production`
   - Set `SESSION_COOKIE_SECURE=True` (requires HTTPS)
   - Set `SECRET_KEY` to a 64-character random hex string (`python -c "import secrets; print(secrets.token_hex(32))"`)
   - Configure live `MONGODB_URI` pointing to your MongoDB Atlas cluster.
   - Run `python scripts/create_indexes.py` once against the cluster.
3. **Frontend CDN**: Static files in `frontend/` can be served directly by Nginx or Cloudflare Pages.

---

## 10. Medical & Ethical Disclaimer

This application is strictly an educational demonstration and scientific study of ensemble machine learning methods.
- The outputs do **not** constitute medical advice or diagnosis.
- Correlation in features does **not** imply medical causation.
- Do not alter prescribed medications, diets, or therapies based on algorithmic outputs.
- In case of chest tightness or cardiovascular distress, contact emergency medical services immediately.

---

## 11. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
