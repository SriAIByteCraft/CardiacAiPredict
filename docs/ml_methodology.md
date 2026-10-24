# Machine Learning Methodology & Experimental Design

## 1. Dataset Provenance & Target Definition

The model is trained and evaluated on the **UCI Cleveland Heart Disease Dataset** (303 instances, 14 attributes), hosted by the UC Irvine Machine Learning Repository.

### Feature Specification
1. **age**: Patient age in years ($[29, 77]$)
2. **sex**: Biological sex ($1 = \text{Male}, 0 = \text{Female}$)
3. **cp**: Chest pain type ($1 = \text{Typical Angina}, 2 = \text{Atypical Angina}, 3 = \text{Non-anginal pain}, 4 = \text{Asymptomatic}$)
4. **trestbps**: Resting blood pressure on admission in mm Hg ($[94, 200]$)
5. **chol**: Serum cholesterol in mg/dl ($[126, 564]$)
6. **fbs**: Fasting blood sugar $> 120 \text{ mg/dl}$ ($1 = \text{True}, 0 = \text{False}$)
7. **restecg**: Resting electrocardiographic results ($0 = \text{Normal}, 1 = \text{ST-T wave abnormality}, 2 = \text{Left ventricular hypertrophy}$)
8. **thalach**: Maximum heart rate achieved during exercise stress test ($[71, 202]$)
9. **exang**: Exercise-induced angina ($1 = \text{Yes}, 0 = \text{No}$)
10. **oldpeak**: ST depression induced by exercise relative to rest in mm ($[0.0, 6.2]$)
11. **slope**: Slope of the peak exercise ST segment ($1 = \text{Upsloping}, 2 = \text{Flat}, 3 = \text{Downsloping}$)
12. **ca**: Number of major coronary vessels colored by fluoroscopy ($[0, 3]$)
13. **thal**: Myocardial perfusion scintigraphy ($3 = \text{Normal}, 6 = \text{Fixed defect}, 7 = \text{Reversible defect}$)

### Target Encoding:
In the raw UCI dataset, `num` takes values $0, 1, 2, 3, 4$, representing the diameter narrowing of coronary vessels ($0 < 50\%$, $1..4 > 50\%$).
We standardize this to a binary classification task:
$$y = \begin{cases} 0 & \text{if } \text{num} = 0 \quad (\text{Absence of significant heart disease}) \\ 1 & \text{if } \text{num} \ge 1 \quad (\text{Presence of heart disease}) \end{cases}$$

---

## 2. Leakage Prevention Protocol

Data leakage can artificially inflate evaluation scores and result in catastrophic failures in clinical deployment. The following safeguards are strictly enforced:

1. **Stratified Partitioning**: The dataset is split into an 80% training set ($n=242$) and a 20% held-out test set ($n=61$), stratified by the binary target to maintain natural prevalence proportions.
2. **Fitting Scope**:
   - `SimpleImputer(strategy='median')` and `StandardScaler()` are fitted **only** on $X_{\text{train}}$.
   - One-hot encoding of categorical attributes is fitted **only** on $X_{\text{train}}$.
   - The test set $X_{\text{test}}$ is transformed using the previously fitted parameters and is never inspected during model tuning.
3. **Resampling Isolation**:
   - SMOTE oversampling and Random Undersampling are applied **only** inside training cross-validation folds using `imblearn.pipeline.Pipeline`. Validation folds and test sets are never resampled.

---

## 3. Stacking Ensemble Classifier

Stacking (Wolpert, 1992) combines predictions from multiple base classifiers through a meta-learner.

### Base Estimators:
1. **Logistic Regression**: $L_2$-regularized linear model providing well-calibrated baseline log-odds.
2. **Random Forest**: Ensemble of 100 de-correlated decision trees capturing non-linear interactions without feature scale sensitivity.
3. **Support Vector Machine**: Radial Basis Function (RBF) kernel maximizing soft margins in infinite-dimensional Hilbert space with Platt probability scaling.

### Meta-Estimator:
- **Logistic Regression**: Takes out-of-fold probability vectors from the three base estimators $[p_{\text{LR}}, p_{\text{RF}}, p_{\text{SVM}}]$ to learn optimal weights without overfitting base estimator training errors.

---

## 4. Class Balancing & Dimensionality Reduction Experiments

In addition to the final pipeline, comprehensive comparative benchmarks are executed across:
1. **Balancing Strategies**:
   - Baseline (None)
   - SMOTE (Synthetic Minority Over-sampling Technique)
   - Random Undersampling (RUS)
   - Cost-Sensitive Class Weighting (`class_weight='balanced'`)
2. **Dimensionality Reduction Strategies**:
   - Baseline (Full 13 Features)
   - Principal Component Analysis (PCA with 10 components)
   - SelectKBest (ANOVA F-statistic top 10 features)
