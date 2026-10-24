/**
 * Central API Client Helper.
 * Handles JSON serialization, session credentials, HTTP status codes, and error toasts.
 */

const API_BASE = '/api';

class APIClient {
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    const config = {
      ...options,
      credentials: 'same-origin', // Sends session cookies
      headers: {
        ...defaultHeaders,
        ...(options.headers || {})
      }
    };

    if (config.body && typeof config.body === 'object') {
      config.body = JSON.stringify(config.body);
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        const errorMsg = data.message || `Request failed with status ${response.status}`;
        const error = new Error(errorMsg);
        error.status = response.status;
        error.code = data.error_code || 'API_ERROR';
        error.details = data.details || null;
        throw error;
      }

      return data;
    } catch (err) {
      // Re-throw for specific caller handling
      throw err;
    }
  }

  get(endpoint, params = {}) {
    const query = new URLSearchParams(params).toString();
    const url = query ? `${endpoint}?${query}` : endpoint;
    return this.request(url, { method: 'GET' });
  }

  post(endpoint, body = {}) {
    return this.request(endpoint, { method: 'POST', body });
  }

  patch(endpoint, body = {}) {
    return this.request(endpoint, { method: 'PATCH', body });
  }

  delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

const api = new APIClient();

// Specialized API Service Wrappers
export const authAPI = {
  register: (payload) => api.post('/auth/register', payload),
  login: (payload) => api.post('/auth/login', payload),
  logout: () => api.post('/auth/logout'),
  getMe: () => api.get('/auth/me')
};

export const predictAPI = {
  predict: (payload) => api.post('/predict', payload)
};

export const historyAPI = {
  getAll: (params) => api.get('/history', params),
  getById: (id) => api.get(`/history/${id}`),
  delete: (id) => api.delete(`/history/${id}`)
};

export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
  getRecent: () => api.get('/dashboard/recent')
};

export const modelAPI = {
  getMetrics: () => api.get('/model/metrics'),
  getComparison: () => api.get('/model/comparison'),
  getHealth: () => api.get('/health'),
  getDbHealth: () => api.get('/database-health')
};

export const profileAPI = {
  get: () => api.get('/profile'),
  update: (payload) => api.patch('/profile', payload),
  changePassword: (payload) => api.post('/profile/change-password', payload)
};

export default api;
