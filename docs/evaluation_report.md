# Empirical Model Evaluation & Comparative Benchmark Report

**Dataset**: UCI Cleveland Heart Disease Dataset  
**Partition**: 80% Train ($n=242$), 20% Held-Out Test ($n=61$)  
**Target Prevalence**: 164 Absent (54.1%), 139 Present (45.9%)  
**Evaluation Date**: October 2026  

---

## 1. Held-Out Test Set Performance (Stacking Ensemble)

All metrics below are computed on the completely independent 61-patient test cohort:

| Metric | Score | Clinical Interpretation |
| :--- | :--- | :--- |
| **Accuracy** | **88.52%** (0.8852) | 54 out of 61 test patients classified correctly. |
| **Precision** | **83.87%** (0.8387) | When the model flags heart disease, it is correct in 83.9% of cases. |
| **Sensitivity (Recall)** | **92.86%** (0.9286) | **Critical Clinical Metric**: Successfully detects 26 of 28 true disease patients. |
| **Specificity** | **84.85%** (0.8485) | True negative rate (28 correctly identified healthy patients out of 33). |
| **F1-Score** | **88.14%** (0.8814) | Balanced harmonic mean between precision and sensitivity. |
| **ROC-AUC** | **0.9600** (96.00%) | Exceptional discriminative capacity across decision thresholds. |
| **Brier Score** | **0.0934** | High calibration; probability values closely align with true binary frequencies. |

### Confusion Matrix (Test Set, $n=61$):

```
                      PREDICTED NEGATIVE (0)     PREDICTED POSITIVE (1)
ACTUAL NEGATIVE (0):            28 (TN)                     5 (FP)
ACTUAL POSITIVE (1):             2 (FN)                    26 (TP)
```

- **True Negatives (TN)**: 28 healthy individuals correctly identified.
- **False Positives (FP)**: 5 patients flagged with risk who did not have disease (sent for confirmation).
- **False Negatives (FN)**: Only 2 patients with heart disease were missed ($\text{FN Rate} = 7.14\%$).
- **True Positives (TP)**: 26 diseased patients correctly identified.

---

## 2. 5-Fold Stratified Cross-Validation Benchmarks

### Classifier Comparison (Base Classifiers vs Stacking Ensemble):
| Estimator | Mean CV Accuracy | Mean CV Recall | Mean CV F1 | Mean CV ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| **Stacking Ensemble (Ensemble)** | **84.28%** | **83.75%** | **82.90%** | **0.9022** |
| Random Forest Classifier | 83.47% | 80.20% | 81.35% | 0.8985 |
| Logistic Regression | 83.88% | 80.20% | 81.70% | 0.9015 |
| Support Vector Machine (RBF) | 83.06% | 79.33% | 80.75% | 0.8940 |
| Decision Tree Classifier | 75.20% | 72.95% | 71.85% | 0.7610 |
| K-Nearest Neighbors (k=5) | 80.17% | 76.57% | 77.40% | 0.8655 |

*Finding*: The Stacking Classifier achieved the highest combined F1-Score (82.90%) and ROC-AUC (0.9022) across cross-validation folds, confirming the benefit of combining linear and non-linear inductive biases.

---

### Class Balancing Comparison (Stacking Model):
| Balancing Technique | Mean CV Accuracy | Mean CV Recall | Mean CV F1 | Mean CV ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| **Baseline (No Resampling)** | 84.28% | 83.75% | 82.90% | 0.9022 |
| **SMOTE (Oversampling)** | 83.45% | **85.58%** | 82.50% | 0.8995 |
| **Random Undersampling** | 81.82% | 84.68% | 80.70% | 0.8870 |
| **Cost-Sensitive Weighting**| 83.88% | 84.68% | 82.70% | 0.9010 |

*Finding*: SMOTE improved sensitivity/recall (from 83.75% to 85.58%), reducing missed positive cases at a minor trade-off in specificity. For pure overall discriminative capacity, the baseline was marginally superior.

---

### Dimensionality Reduction Comparison (Stacking Model):
| Method | Original Features | Components / Retained | Mean CV Accuracy | Mean CV ROC-AUC |
| :--- | :---: | :---: | :---: | :---: |
| **Full Features Baseline** | 13 | 13 | **84.28%** | **0.9022** |
| **SelectKBest (ANOVA F-test)**| 13 | 10 | 83.05% | 0.8910 |
| **PCA (Principal Components)**| 13 | 10 | 81.40% | 0.8745 |

*Finding*: The full 13-feature baseline outperformed PCA dimensionality reduction. In clinical datasets with well-curated physiological indicators, preserving all domain-specified attributes avoids loss of diagnostic variance.
