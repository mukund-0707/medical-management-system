import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Main axios instance
const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Request interceptor — attach JWT token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('msms_access');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor — auto-refresh on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;

    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem('msms_refresh');

      if (refresh) {
        try {
          const res = await axios.post(`${BASE_URL}/auth/refresh/`, { refresh });
          const newAccess = res.data.data.access;
          const newRefresh = res.data.data.refresh;
          localStorage.setItem('msms_access', newAccess);
          localStorage.setItem('msms_refresh', newRefresh);
          original.headers.Authorization = `Bearer ${newAccess}`;
          return api(original);
        } catch {
          // Refresh failed — clear tokens and redirect to login
          localStorage.removeItem('msms_access');
          localStorage.removeItem('msms_refresh');
          localStorage.removeItem('msms_user');
          window.location.href = '/login';
        }
      } else {
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;

// ── Auth ──────────────────────────────────────────────────
export const authAPI = {
  login:   (username, password) => api.post('/auth/login/', { username, password }),
  logout:  (refresh) => api.post('/auth/logout/', { refresh }),
  me:      () => api.get('/auth/me/'),
};

// ── Dashboard ─────────────────────────────────────────────
export const dashboardAPI = {
  kpi:       (date) => api.get('/dashboard/', { params: date ? { date } : {} }),
  sales:     (params) => api.get('/dashboard/sales/', { params }),
  purchases: (params) => api.get('/dashboard/purchases/', { params }),
  inventory: () => api.get('/dashboard/inventory/'),
  alerts:    () => api.get('/dashboard/alerts/'),
};

// ── Medicine ──────────────────────────────────────────────
export const medicineAPI = {
  list:    (params) => api.get('/medicines/', { params }),
  get:     (id) => api.get(`/medicines/${id}/`),
  create:  (data) => api.post('/medicines/', data),
  update:  (id, data) => api.patch(`/medicines/${id}/`, data),
  delete:  (id) => api.delete(`/medicines/${id}/`),
  barcode: (code) => api.get(`/medicines/barcode/${code}/`),
};

// ── Supplier ──────────────────────────────────────────────
export const supplierAPI = {
  list:   (params) => api.get('/suppliers/', { params }),
  get:    (id) => api.get(`/suppliers/${id}/`),
  create: (data) => api.post('/suppliers/', data),
  update: (id, data) => api.patch(`/suppliers/${id}/`, data),
  delete: (id) => api.delete(`/suppliers/${id}/`),
};

// ── Purchase ──────────────────────────────────────────────
export const purchaseAPI = {
  list:     (params) => api.get('/purchases/', { params }),
  get:      (id) => api.get(`/purchases/${id}/`),
  create:   (data) => api.post('/purchases/', data),
  update:   (id, data) => api.patch(`/purchases/${id}/`, data),
  finalize: (id) => api.post(`/purchases/${id}/finalize/`),
  cancel:   (id) => api.post(`/purchases/${id}/cancel/`),
};

// ── Inventory ─────────────────────────────────────────────
export const inventoryAPI = {
  batches:    (params) => api.get('/inventory/batches/', { params }),
  getBatch:   (id) => api.get(`/inventory/batches/${id}/`),
  adjust:     (data) => api.post('/inventory/adjust/', data),
  markExpired:(id) => api.post(`/inventory/batches/${id}/mark-expired/`),
  ledger:     (params) => api.get('/inventory/ledger/', { params }),
  stock:      (medicineId) => api.get(`/inventory/stock/${medicineId}/`),
};

// ── Billing ───────────────────────────────────────────────
export const billingAPI = {
  createSession: () => api.post('/billing/sessions/'),
  getSession:    (id) => api.get(`/billing/sessions/${id}/`),
  cancelSession: (id) => api.delete(`/billing/sessions/${id}/`),
  addItem:       (sessionId, data) => api.post(`/billing/sessions/${sessionId}/items/`, data),
  updateItem:    (sessionId, itemId, data) => api.patch(`/billing/sessions/${sessionId}/items/${itemId}/`, data),
  removeItem:    (sessionId, itemId) => api.delete(`/billing/sessions/${sessionId}/items/${itemId}/`),
};

// ── Sales ─────────────────────────────────────────────────
export const salesAPI = {
  list:      (params) => api.get('/sales/', { params }),
  get:       (id) => api.get(`/sales/${id}/`),
  checkout:  (data) => api.post('/sales/checkout/', data),
  cancel:    (id) => api.post(`/sales/${id}/cancel/`),
  byInvoice: (inv) => api.get(`/sales/invoice/${inv}/`),
};

// ── Reports ───────────────────────────────────────────────
export const reportsAPI = {
  sales:       (params) => api.get('/reports/sales/', { params }),
  purchases:   (params) => api.get('/reports/purchases/', { params }),
  inventory:   (params) => api.get('/reports/inventory/', { params }),
  ledger:      (params) => api.get('/reports/ledger/', { params }),
  expiry:      (days) => api.get('/reports/expiry/', { params: { days } }),
  lowStock:    (threshold) => api.get('/reports/low-stock/', { params: { threshold } }),
  adjustments: (params) => api.get('/reports/adjustments/', { params }),
  medicines:   (params) => api.get('/reports/medicines/', { params }),
  suppliers:   (params) => api.get('/reports/suppliers/', { params }),
};
