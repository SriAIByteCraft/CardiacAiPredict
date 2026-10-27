/**
 * Dashboard Controller.
 * Loads statistics, renders Chart.js timeline, and displays recent predictions.
 */

import { requireAuth } from './auth.js';
import { dashboardAPI } from './api.js';
import { showToast, formatDateTime } from './ui.js';

let activityChartInstance = null;

export async function initDashboard() {
  const user = await requireAuth();
  
  // Greet user
  const welcomeName = document.getElementById('user-welcome-name');
  if (welcomeName && user.name) {
    welcomeName.textContent = user.name;
  }

  loadStats();
  loadRecentPredictions();
}

async function loadStats() {
  try {
    const res = await dashboardAPI.getStats();
    const stats = res.data;

    // Update KPIs
    setText('stat-total-predictions', stats.total_predictions);
    setText('stat-elevated-risk', stats.elevated_risk_count);
    setText('stat-low-risk', stats.low_risk_count);
    
    const acc = typeof stats.model_accuracy === 'number' 
      ? `${(stats.model_accuracy * 100).toFixed(1)}%` 
      : stats.model_accuracy;
    setText('stat-model-accuracy', acc);

    // Render Activity Chart
    renderActivityChart(stats.activity_timeline || []);
  } catch (err) {
    showToast('Failed to load dashboard metrics: ' + err.message, 'error');
  }
}

async function loadRecentPredictions() {
  const tableBody = document.getElementById('recent-predictions-tbody');
  const emptyState = document.getElementById('recent-empty-state');
  if (!tableBody) return;

  try {
    const res = await dashboardAPI.getRecent();
    const recent = res.data?.recent_predictions || [];

    tableBody.innerHTML = '';

    if (recent.length === 0) {
      if (emptyState) emptyState.style.display = 'block';
      return;
    }

    if (emptyState) emptyState.style.display = 'none';

    recent.forEach((item) => {
      const tr = document.createElement('tr');

      // Date
      const tdDate = document.createElement('td');
      tdDate.textContent = formatDateTime(item.created_at);
      tr.appendChild(tdDate);

      // Patient Identity & Vitals Summary
      const tdVitals = document.createElement('td');
      const feats = item.validated_features || {};
      const sexLabel = feats.sex === 1 ? 'Male' : 'Female';
      const pName = document.createElement('div');
      pName.style.fontWeight = '700';
      pName.textContent = item.patient_name || 'Anonymous Patient';
      const pMeta = document.createElement('div');
      pMeta.className = 'text-muted';
      pMeta.style.fontSize = '0.78rem';
      pMeta.textContent = `${feats.age || 'N/A'} yrs, ${sexLabel} | BP: ${feats.trestbps || 'N/A'} mmHg`;
      tdVitals.appendChild(pName);
      tdVitals.appendChild(pMeta);
      tr.appendChild(tdVitals);

      // Prediction Label
      const tdPred = document.createElement('td');
      tdPred.textContent = item.prediction_label || (item.prediction === 1 ? 'Disease Risk' : 'No Disease');
      tr.appendChild(tdPred);

      // Risk Badge
      const tdRisk = document.createElement('td');
      const badge = document.createElement('span');
      const badgeClass = item.prediction === 1 ? 'badge risk-high' : 'badge risk-low';
      badge.className = badgeClass;
      badge.textContent = item.risk_level || (item.prediction === 1 ? 'Elevated' : 'Low');
      tdRisk.appendChild(badge);
      tr.appendChild(tdRisk);

      // Probability
      const tdProb = document.createElement('td');
      tdProb.textContent = typeof item.probability === 'number' 
        ? `${(item.probability * 100).toFixed(1)}%` 
        : 'N/A';
      tr.appendChild(tdProb);

      // Action Link
      const tdAction = document.createElement('td');
      const viewLink = document.createElement('a');
      viewLink.href = `result.html?id=${item.id}`;
      viewLink.className = 'btn btn-outline btn-sm';
      viewLink.textContent = 'View Report';
      tdAction.appendChild(viewLink);
      tr.appendChild(tdAction);

      tableBody.appendChild(tr);
    });
  } catch (err) {
    showToast('Failed to load recent activity: ' + err.message, 'error');
  }
}

function renderActivityChart(timeline) {
  const canvas = document.getElementById('activity-chart');
  if (!canvas || typeof Chart === 'undefined') return;

  const labels = timeline.map(t => t.date);
  const dataCounts = timeline.map(t => t.count);

  if (activityChartInstance) {
    activityChartInstance.destroy();
  }

  const ctx = canvas.getContext('2d');
  activityChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Predictions Run',
        data: dataCounts,
        borderColor: '#0284c7',
        backgroundColor: 'rgba(2, 132, 199, 0.1)',
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
        pointBackgroundColor: '#0284c7',
        pointRadius: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: { precision: 0 },
          grid: { color: '#f1f5f9' }
        },
        x: {
          grid: { display: false }
        }
      }
    }
  });
}

function setText(elementId, text) {
  const el = document.getElementById(elementId);
  if (el) el.textContent = text !== null && text !== undefined ? text : '0';
}

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('dashboard-view')) {
    initDashboard();
  }
});
