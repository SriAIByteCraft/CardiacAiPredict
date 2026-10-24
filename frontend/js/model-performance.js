/**
 * Model Performance and Comparative Benchmarking Controller.
 * Loads actual saved evaluation metrics and renders interactive Chart.js visualizations
 * for Base Models, Balancing Techniques, and Dimensionality Reduction.
 */

import { modelAPI } from './api.js';
import { showToast } from './ui.js';

let rocChartInstance = null;
let modelsChartInstance = null;
let balancingChartInstance = null;
let reductionChartInstance = null;

export async function initPerformancePage() {
  loadMetrics();
  loadComparison();
}

async function loadMetrics() {
  try {
    const res = await modelAPI.getMetrics();
    const meta = res.data;
    const test = meta.test_metrics || {};

    // 1. Metric Scoreboard Cards
    setScore('score-accuracy', test.accuracy);
    setScore('score-precision', test.precision);
    setScore('score-recall', test.recall);
    setScore('score-specificity', test.specificity);
    setScore('score-f1', test.f1_score);
    setScore('score-roc-auc', test.roc_auc);

    // Metadata descriptions
    const verEl = document.getElementById('perf-model-version');
    if (verEl) verEl.textContent = `Version ${meta.version || '1.0.0'} (${meta.model_name})`;

    const trainEl = document.getElementById('perf-trained-at');
    if (trainEl && meta.trained_at) {
      trainEl.textContent = new Date(meta.trained_at).toLocaleDateString('en-US', {
        year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
      });
    }

    // 2. Render Confusion Matrix Heat Cells
    const cm = test.confusion_matrix || {};
    setText('cm-tn', cm.true_negatives);
    setText('cm-fp', cm.false_positives);
    setText('cm-fn', cm.false_negatives);
    setText('cm-tp', cm.true_positives);

    // 3. Render ROC Curve
    if (test.roc_curve) {
      renderRocCurve(test.roc_curve, test.roc_auc);
    }

    // 4. Render Feature Importances
    renderFeatureImportance(meta.explainability?.top_features || []);

  } catch (err) {
    showToast('Failed to load model metrics: ' + err.message, 'error');
  }
}

async function loadComparison() {
  try {
    const res = await modelAPI.getComparison();
    const comp = res.data;

    // 1. Classifiers Comparison Chart
    renderClassifiersChart(comp.models_comparison || []);

    // 2. Balancing Techniques Comparison Chart
    renderBalancingChart(comp.balancing_comparison || []);

    // 3. Dimensionality Reduction Comparison Chart
    renderReductionChart(comp.reduction_comparison || []);

  } catch (err) {
    showToast('Failed to load comparative benchmarks: ' + err.message, 'error');
  }
}

function renderRocCurve(rocData, aucVal) {
  const canvas = document.getElementById('roc-curve-chart');
  if (!canvas || typeof Chart === 'undefined') return;

  const points = rocData.fpr.map((fpr, i) => ({
    x: fpr,
    y: rocData.tpr[i]
  }));

  if (rocChartInstance) rocChartInstance.destroy();

  rocChartInstance = new Chart(canvas.getContext('2d'), {
    type: 'scatter',
    data: {
      datasets: [
        {
          label: `Stacking Ensemble (AUC = ${aucVal !== undefined ? aucVal : 'N/A'})`,
          data: points,
          showLine: true,
          borderColor: '#0284c7',
          backgroundColor: 'rgba(2, 132, 199, 0.1)',
          borderWidth: 2.5,
          fill: true,
          pointRadius: 2
        },
        {
          label: 'Chance Line (AUC = 0.50)',
          data: [{ x: 0, y: 0 }, { x: 1, y: 1 }],
          showLine: true,
          borderColor: '#94a3b8',
          borderDash: [5, 5],
          borderWidth: 1.5,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: {
          title: { display: true, text: 'False Positive Rate (1 - Specificity)' },
          min: 0,
          max: 1
        },
        y: {
          title: { display: true, text: 'True Positive Rate (Sensitivity / Recall)' },
          min: 0,
          max: 1
        }
      }
    }
  });
}

function renderClassifiersChart(models) {
  const canvas = document.getElementById('models-comparison-chart');
  if (!canvas || typeof Chart === 'undefined' || models.length === 0) return;

  const labels = models.map(m => {
    const nameMap = {
      logistic_regression: 'Logistic Regression',
      random_forest: 'Random Forest',
      svm: 'Support Vector Machine',
      decision_tree: 'Decision Tree',
      knn: 'K-Nearest Neighbors',
      stacking_ensemble: '★ Stacking Ensemble'
    };
    return nameMap[m.model_name] || m.model_name;
  });

  const accuracyData = models.map(m => m.accuracy * 100);
  const f1Data = models.map(m => m.f1_score * 100);

  if (modelsChartInstance) modelsChartInstance.destroy();

  modelsChartInstance = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Accuracy (%)',
          data: accuracyData,
          backgroundColor: '#0284c7'
        },
        {
          label: 'F1-Score (%)',
          data: f1Data,
          backgroundColor: '#0d9488'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: false, min: 60, max: 100, title: { display: true, text: 'Score (%)' } }
      }
    }
  });
}

function renderBalancingChart(balancing) {
  const canvas = document.getElementById('balancing-comparison-chart');
  if (!canvas || typeof Chart === 'undefined' || balancing.length === 0) return;

  const labels = balancing.map(b => b.technique);
  const recallData = balancing.map(b => b.recall * 100);
  const rocData = balancing.map(b => (b.roc_auc || 0) * 100);

  if (balancingChartInstance) balancingChartInstance.destroy();

  balancingChartInstance = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Recall / Sensitivity (%)',
          data: recallData,
          backgroundColor: '#f59e0b'
        },
        {
          label: 'ROC-AUC (%)',
          data: rocData,
          backgroundColor: '#0284c7'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: false, min: 60, max: 100, title: { display: true, text: 'Metric (%)' } }
      }
    }
  });
}

function renderReductionChart(reduction) {
  const canvas = document.getElementById('reduction-comparison-chart');
  if (!canvas || typeof Chart === 'undefined' || reduction.length === 0) return;

  const labels = reduction.map(r => r.technique);
  const accData = reduction.map(r => r.accuracy * 100);
  const rocData = reduction.map(r => (r.roc_auc || 0) * 100);

  if (reductionChartInstance) reductionChartInstance.destroy();

  reductionChartInstance = new Chart(canvas.getContext('2d'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Accuracy (%)',
          data: accData,
          backgroundColor: '#0d9488'
        },
        {
          label: 'ROC-AUC (%)',
          data: rocData,
          backgroundColor: '#6366f1'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: false, min: 60, max: 100, title: { display: true, text: 'Score (%)' } }
      }
    }
  });
}

function renderFeatureImportance(features) {
  const container = document.getElementById('feature-importance-list');
  if (!container || features.length === 0) return;

  container.innerHTML = '';
  const maxImp = Math.max(...features.map(f => f.importance_mean || 0.01), 0.01);

  features.forEach(feat => {
    const pct = Math.max(5, (feat.importance_mean / maxImp) * 100);
    const row = document.createElement('div');
    row.style.marginBottom = '0.85rem';
    row.innerHTML = `
      <div style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:0.25rem;">
        <strong>${feat.feature}</strong>
        <span class="text-muted">+${(feat.importance_mean * 100).toFixed(2)}% AUC drop</span>
      </div>
      <div style="height: 8px; background:#e2e8f0; border-radius:4px; overflow:hidden;">
        <div style="width: ${pct}%; height: 100%; background: var(--primary); border-radius:4px;"></div>
      </div>
    `;
    container.appendChild(row);
  });
}

function setScore(id, val) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = typeof val === 'number' ? `${(val * 100).toFixed(1)}%` : (val || 'N/A');
  }
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text !== undefined ? text : '0';
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('performance-view')) {
    initPerformancePage();
  }
});
