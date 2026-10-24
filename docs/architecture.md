# System Architecture & Technical Specifications

## 1. System Overview

**CardioPredict** is a production-grade, full-stack clinical machine learning web application engineered for cardiovascular risk estimation using a heterogeneous Stacking Ensemble classifier, class balancing methods (SMOTE, Random Undersampling), dimensionality reduction (PCA, SelectKBest), and MongoDB Atlas persistence.

```
+-----------------------------------------------------------------------------------+
|                                  USER / BROWSER                                    |
|   HTML5 + Vanilla JavaScript (ES Modules) + Custom CSS3 Design System + Chart.js  |
+------------------------------------------+----------------------------------------+
                                           | HTTP / REST API (JSON)
                                           v
+-----------------------------------------------------------------------------------+
|                             FLASK APPLICATION SERVER                              |
|                                                                                   |
|  [Middleware Layer]                                                               |
|  - Auth Session Middleware (@login_required)                                      |
|  - Rate Limiter (Token Bucket / Sliding Window)                                   |
|  - OWASP Defensive Security Headers (CSP, FrameGuard, NoSniff)                    |
|                                                                                   |
|  [Modular API Blueprints (/api)]                                                  |
|  +------------------+  +------------------+  +------------------+                 |
|  |   Auth Routes    |  |  Profile Routes  |  | Predict Routes   |                 |
|  +------------------+  +------------------+  +------------------+                 |
|  +------------------+  +------------------+  +------------------+                 |
|  |  History Routes  |  | Dashboard Routes |  |  Model & Health  |                 |
|  +------------------+  +------------------+  +------------------+                 |
|                                                                                   |
|  [Service Layer]                                                                  |
|  - AuthService, UserService, PredictionService, HistoryService, ModelService      |
|                                                                                   |
|  [Machine Learning Inference Engine]                                              |
|  - Model Artifact Loader (joblib bundle)                                          |
|  - Input Validation & Bounds Enforcement (13 UCI features)                        |
|  - Fitted Scikit-Learn Preprocessing Pipeline (StandardScaler + OneHotEncoder)    |
|  - StackingClassifier (LR + RF + SVM -> Meta Logistic Regression)                 |
|  - Calibrated Probability & Risk Tier Calculation                                 |
+---------------------+-------------------------------------+-----------------------+
                      |                                     |
                      v                                     v
+------------------------------------+   +------------------------------------------+
|       MONGODB ATLAS DATABASE       |   |             LOCAL ARTIFACTS              |
|  - users collection (unique email) |   |  - stacking_heart_model.joblib           |
|  - predictions collection (history)|   |  - model_metrics.json                    |
|  - model_metrics collection        |   |  - model_comparison.json                |
|  (with in-memory fallback for test)|   |  - ROC curve & Confusion Matrix plots    |
+------------------------------------+   +------------------------------------------+
```

## 2. Key Modules

### Frontend
- **Vanilla JavaScript Modular Architecture**: No heavyweight JS frameworks required; fast load times and clean separation of concerns.
- **Central API Helper (`api.js`)**: Encapsulates fetch requests with session awareness (`credentials: 'same-origin'`), response parsing, and error interception.
- **Chart.js Visualizations**: Interactive line/bar charts on the dashboard and multi-model ROC/PR curves on the performance page.

### Backend
- **Application Factory Pattern (`app.py`)**: Supports multiple configurations (`development`, `testing`, `production`).
- **Flask Blueprints**: High degree of modularity across domain boundaries.
- **PyMongo & MongoDB Atlas**: Cloud-native document storage with unique email indexing and user-scoped prediction history. Graceful in-memory fallback (`mongomock`) for offline use and automated tests.

### Machine Learning
- **Zero-Leakage Training Pipeline**: Preprocessing, scaling, one-hot encoding, feature selection, and resampling fitted strictly on training data folds.
- **Ensemble Diversity**:
  - Linear Model: Logistic Regression (L2 penalty)
  - Bagging Tree: Random Forest (100 estimators, max depth 5)
  - Kernel Method: Support Vector Machine (RBF kernel, probability estimation)
  - Meta-Learner: Cross-validated out-of-fold Logistic Regression.
