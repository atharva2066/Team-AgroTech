/* =============================================
   AgroChar — API Service Layer
   Maps to: frontend/src/services/api.js
             frontend/src/services/advisoryService.js
             frontend/src/services/buyerService.js
   Backend:  FastAPI at /api/v1/*
   ============================================= */

'use strict';

// ─────────────────────────────────────────────
// CONFIG  (matches backend/app/core/config.py)
// ─────────────────────────────────────────────
const CONFIG = {
  BASE_URL:    'http://localhost:8000/api/v1',   // swap with env var in prod
  TIMEOUT_MS:  12000,
  TOKEN_KEY:   'agrochar_token',
  ROLE_KEY:    'agrochar_role',
};

// ─────────────────────────────────────────────
// TOKEN HELPERS  (security.py → JWT)
// ─────────────────────────────────────────────
const Auth = {
  getToken()          { return localStorage.getItem(CONFIG.TOKEN_KEY); },
  setToken(token)     { localStorage.setItem(CONFIG.TOKEN_KEY, token); },
  getRole()           { return localStorage.getItem(CONFIG.ROLE_KEY); },
  setRole(role)       { localStorage.setItem(CONFIG.ROLE_KEY, role); },
  clear()             { localStorage.removeItem(CONFIG.TOKEN_KEY); localStorage.removeItem(CONFIG.ROLE_KEY); },
  isLoggedIn()        { return !!this.getToken(); },
};

// ─────────────────────────────────────────────
// BASE HTTP CLIENT
// ─────────────────────────────────────────────
async function request(method, path, body = null, opts = {}) {
  const url = `${CONFIG.BASE_URL}${path}`;
  const token = Auth.getToken();

  const headers = {
    'Content-Type': 'application/json',
    ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
    ...opts.headers,
  };

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), CONFIG.TIMEOUT_MS);

  try {
    const res = await fetch(url, {
      method,
      headers,
      signal: controller.signal,
      ...(body ? { body: JSON.stringify(body) } : {}),
    });

    clearTimeout(timeout);

    // 401 → redirect to login
    if (res.status === 401) {
      Auth.clear();
      window.location.href = '/login.html';
      return;
    }

    const data = await res.json();

    if (!res.ok) {
      throw new APIError(data.detail || 'Request failed', res.status, data);
    }

    return data;

  } catch (err) {
    clearTimeout(timeout);
    if (err.name === 'AbortError') throw new APIError('Request timed out', 408);
    throw err;
  }
}

class APIError extends Error {
  constructor(message, status, data = null) {
    super(message);
    this.status = status;
    this.data = data;
  }
}

const http = {
  get:    (path, opts)       => request('GET',    path, null, opts),
  post:   (path, body, opts) => request('POST',   path, body, opts),
  put:    (path, body, opts) => request('PUT',     path, body, opts),
  delete: (path, opts)       => request('DELETE', path, null, opts),
};

// ─────────────────────────────────────────────
// ADVISORY SERVICE
// Maps to: backend/app/api/routes/advisory.py
//          backend/app/services/residue_service.py
//          backend/app/services/financial_service.py
//          backend/app/services/ranking_service.py
// ─────────────────────────────────────────────
const AdvisoryService = {

  /**
   * POST /advisory/analyze
   * Body: { field_size_acres, crop_type, location_district, state }
   * Returns: ranked list of alternatives with financials
   * → residue_service.py → financial_service.py → ranking_service.py
   */
  async analyze(formData) {
    return http.post('/advisory/analyze', {
      field_size_acres:    parseFloat(formData.fieldSize),
      crop_type:           formData.cropType,
      location_district:   formData.location,
      state:               formData.state || 'Punjab',
    });
  },

  /**
   * GET /advisory/alternatives
   * Returns all supported alternative types with metadata
   */
  async getAlternatives() {
    return http.get('/advisory/alternatives');
  },

  /**
   * GET /advisory/history/{farmer_id}
   * Returns past advisory requests for logged-in farmer
   */
  async getHistory(farmerId) {
    return http.get(`/advisory/history/${farmerId}`);
  },

  /**
   * GET /advisory/carbon-credits?district=X&crop=Y
   * → ml/price_model.py for credit price prediction
   */
  async getCarbonCreditEstimate(district, cropType) {
    return http.get(`/advisory/carbon-credits?district=${district}&crop=${cropType}`);
  },
};

// ─────────────────────────────────────────────
// FARMER SERVICE
// Maps to: backend/app/api/routes/farmer.py
//          backend/app/models/farmer.py
// ─────────────────────────────────────────────
const FarmerService = {

  /**
   * GET /farmer/profile
   * Returns logged-in farmer's profile
   */
  async getProfile() {
    return http.get('/farmer/profile');
  },

  /**
   * GET /farmer/dashboard-summary
   * Returns KPI stats for the farmer dashboard header
   */
  async getDashboardSummary() {
    return http.get('/farmer/dashboard-summary');
  },

  /**
   * GET /farmer/fields
   * Returns list of farmer's registered fields
   */
  async getFields() {
    return http.get('/farmer/fields');
  },

  /**
   * POST /farmer/fields
   * Register a new field
   */
  async addField(fieldData) {
    return http.post('/farmer/fields', fieldData);
  },

  /**
   * GET /farmer/earnings
   * Returns earnings summary for the farmer
   */
  async getEarnings() {
    return http.get('/farmer/earnings');
  },
};

// ─────────────────────────────────────────────
// BUYER SERVICE
// Maps to: backend/app/api/routes/buyer.py
//          backend/app/services/buyer_matching_service.py
// ─────────────────────────────────────────────
const BuyerService = {

  /**
   * GET /buyers/nearby?district=X&type=biochar&radius_km=100
   * Returns sorted list of buyers near farmer
   * → buyer_matching_service.py
   */
  async getNearbyBuyers(district, type = null, radiusKm = 100) {
    const params = new URLSearchParams({ district, radius_km: radiusKm });
    if (type) params.set('type', type);
    return http.get(`/buyers/nearby?${params}`);
  },

  /**
   * GET /buyers/listings?type=X&district=Y
   * Returns active supply listings visible to buyers
   */
  async getListings(filters = {}) {
    const params = new URLSearchParams(filters);
    return http.get(`/buyers/listings?${params}`);
  },

  /**
   * POST /buyers/bid
   * Submit a bid on a listing
   */
  async submitBid(listingId, pricePerKg, quantityKg) {
    return http.post('/buyers/bid', { listing_id: listingId, price_per_kg: pricePerKg, quantity_kg: quantityKg });
  },

  /**
   * GET /buyers/orders?status=X
   * Returns buyer's active & historical orders
   */
  async getOrders(status = null) {
    const params = status ? `?status=${status}` : '';
    return http.get(`/buyers/orders${params}`);
  },

  /**
   * GET /buyers/dashboard-summary
   * Returns KPI summary for buyer dashboard
   */
  async getDashboardSummary() {
    return http.get('/buyers/dashboard-summary');
  },

  /**
   * POST /buyers/connect
   * Send a connection request to a farmer
   */
  async connectWithFarmer(farmerId, message) {
    return http.post('/buyers/connect', { farmer_id: farmerId, message });
  },

  /**
   * GET /buyers/alerts
   * Returns alert notifications for buyer
   */
  async getAlerts() {
    return http.get('/buyers/alerts');
  },

  /**
   * GET /buyers/pricing-trends?type=X
   * → ml/price_model.py
   */
  async getPricingTrends(type) {
    return http.get(`/buyers/pricing-trends?type=${type}`);
  },
};

// ─────────────────────────────────────────────
// ADMIN / ANALYTICS SERVICE
// Maps to: backend/app/api/routes/admin.py
//          analytics/event_tracking.py
// ─────────────────────────────────────────────
const AdminService = {

  /**
   * GET /admin/analytics/overview
   * Returns platform-wide KPIs
   */
  async getOverview() {
    return http.get('/admin/analytics/overview');
  },

  /**
   * GET /admin/analytics/monthly?year=2024
   * Returns monthly residue + revenue data for trend chart
   */
  async getMonthlyTrends(year = new Date().getFullYear()) {
    return http.get(`/admin/analytics/monthly?year=${year}`);
  },

  /**
   * GET /admin/analytics/by-district
   * Returns district-wise performance table
   */
  async getDistrictStats() {
    return http.get('/admin/analytics/by-district');
  },

  /**
   * GET /admin/analytics/co2
   * Returns CO2 avoidance data
   */
  async getCO2Stats() {
    return http.get('/admin/analytics/co2');
  },

  /**
   * GET /admin/analytics/alternative-mix
   * Returns breakdown by alternative type
   */
  async getAlternativeMix() {
    return http.get('/admin/analytics/alternative-mix');
  },
};

// ─────────────────────────────────────────────
// CROP SERVICE
// Maps to: backend/app/models/crop.py
//          database/seed_data/crop_ratios.csv
// ─────────────────────────────────────────────
const CropService = {
  /**
   * GET /crops
   * Returns all supported crop types
   */
  async getCrops() {
    return http.get('/crops');
  },
};

// ─────────────────────────────────────────────
// AUTH SERVICE
// Maps to: backend/app/core/security.py
// ─────────────────────────────────────────────
const AuthService = {

  /**
   * POST /auth/login
   * Returns JWT token + user role
   */
  async login(email, password) {
    const data = await http.post('/auth/login', { email, password });
    Auth.setToken(data.access_token);
    Auth.setRole(data.role);
    return data;
  },

  /**
   * POST /auth/logout
   */
  async logout() {
    try { await http.post('/auth/logout'); } catch(_) {}
    Auth.clear();
    window.location.href = '/login.html';
  },

  async getMe() {
    return http.get('/auth/me');
  },
};

// ─────────────────────────────────────────────
// UI HELPERS
// ─────────────────────────────────────────────
const UI = {

  // Show toast notification
  toast(message, type = 'info', duration = 3500) {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const icons = { success: '✅', error: '❌', info: 'ℹ️' };
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<span>${icons[type]}</span><span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => toast.remove(), duration);
  },

  // Set loading state on a button
  setLoading(btn, loading, originalText) {
    if (loading) {
      btn.disabled = true;
      btn.dataset.original = btn.textContent;
      btn.textContent = 'Loading...';
    } else {
      btn.disabled = false;
      btn.textContent = originalText || btn.dataset.original;
    }
  },

  // Render skeleton placeholder rows
  renderSkeletons(container, count, height = 40) {
    container.innerHTML = Array.from({ length: count }, () =>
      `<div class="skeleton" style="height:${height}px;margin-bottom:10px;"></div>`
    ).join('');
  },

  // Format currency in Indian rupees
  formatINR(amount) {
    if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(1)}Cr`;
    if (amount >= 100000)   return `₹${(amount / 100000).toFixed(1)}L`;
    if (amount >= 1000)     return `₹${(amount / 1000).toFixed(1)}k`;
    return `₹${amount}`;
  },

  // Format date
  formatDate(dateStr) {
    return new Date(dateStr).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' });
  },
};

// ─────────────────────────────────────────────
// MOCK DATA  (used when backend not available)
// Remove this section once API is live.
// ─────────────────────────────────────────────
const MOCK = {

  advisoryResult: {
    residue_tonnes: 9.6,
    alternatives: [
      { type: 'biochar',      name: 'Biochar Production',    icon: '🪨', setup_cost: 45000, annual_income: 54000, breakeven_months: 11, viability_pct: 88, is_best: true,  desc: 'Convert rice straw into biochar using a pyrolysis unit. Earns carbon credits.' },
      { type: 'pellets',      name: 'Pellet Manufacturing',  icon: '🔩', setup_cost: 120000, annual_income: 72000, breakeven_months: 20, viability_pct: 72, is_best: false, desc: 'Compress straw into fuel pellets for industrial boilers and biomass plants.' },
      { type: 'composting',   name: 'Composting',            icon: '♻️', setup_cost: 12000, annual_income: 24000, breakeven_months: 6,  viability_pct: 60, is_best: false, desc: 'Mix straw with cow dung to produce organic compost, cutting fertilizer spend.' },
      { type: 'direct',       name: 'Direct Incorporation',  icon: '🌱', setup_cost: 8000,  annual_income: 18000, breakeven_months: 5,  viability_pct: 52, is_best: false, desc: 'Incorporate straw directly into soil for long-term health improvement.' },
    ],
    roadmap: [
      { month: 'Month 1',  text: 'Apply for PM-KUSUM subsidy & contact biochar kiln supplier' },
      { month: 'Month 2',  text: 'Install pyrolysis kiln, train workers, sign supply agreement' },
      { month: 'Month 3–5',text: 'First batch production. Apply biochar to 30% of field' },
      { month: 'Month 6',  text: 'Register for Voluntary Carbon Credits (₹8k–₹12k/yr extra)' },
      { month: 'Month 11', text: '🎉 Break-even achieved. Pure profit from Month 12 onwards' },
    ],
  },

  nearbyBuyers: [
    { id: 1, name: 'Punjab Agro Biochar Co.',   type: 'biochar',    distance_km: 12, price_per_kg: 6.50, location: 'Ludhiana' },
    { id: 2, name: 'GreenPower Pellets Pvt.',   type: 'pellets',    distance_km: 23, price_per_kg: 4.20, location: 'Jalandhar' },
    { id: 3, name: 'OrganicLink Aggregator',    type: 'composting', distance_km:  8, price_per_kg: 3.80, location: 'Ludhiana' },
  ],

  buyerListings: [
    { id: 1, farmer: 'Rajan Singh',       initials: 'RS', location: 'Ludhiana',  type: 'biochar',  qty_kg: 320,  price_per_kg: 6.20, distance_km: 12, status: 'ready' },
    { id: 2, farmer: 'Amarjeet Mann',     initials: 'AM', location: 'Amritsar',  type: 'pellets',  qty_kg: 1200, price_per_kg: 4.10, distance_km: 38, status: 'ready' },
    { id: 3, farmer: 'Preet Kaur',        initials: 'PK', location: 'Patiala',   type: 'compost',  qty_kg: 800,  price_per_kg: 3.70, distance_km: 54, status: 'pending' },
    { id: 4, farmer: 'Gurmail Singh',     initials: 'GS', location: 'Sangrur',   type: 'biochar',  qty_kg: 2100, price_per_kg: 5.90, distance_km: 67, status: 'ready' },
    { id: 5, farmer: 'Harvinder Dhillon', initials: 'HD', location: 'Ferozepur', type: 'pellets',  qty_kg: 500,  price_per_kg: 4.35, distance_km: 82, status: 'low' },
  ],

  analyticsOverview: {
    farmers_onboarded: 4821,
    tonnes_diverted:   12400,
    revenue_inr:       38000000,
    active_buyers:     312,
    co2_saved_tonnes:  8240,
  },

  monthlyTrends: {
    labels:   ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov'],
    tonnes:   [420, 580, 410, 620, 780, 920, 860, 1100, 1420, 2100, 1900],
    revenue:  [8,   12,  9,   11,  14,  18,  16,  22,   28,   42,   38],
  },
};

// ─────────────────────────────────────────────
// FEATURE FLAG: use mock data when API is down
// Set AGROCHAR_USE_MOCK=false in prod
// ─────────────────────────────────────────────
const USE_MOCK = true; // ← flip to false when backend is live

// Wrap services with mock fallback
function withMock(service, mockKey) {
  return new Proxy(service, {
    get(target, prop) {
      if (!USE_MOCK || typeof target[prop] !== 'function') return target[prop];
      return async (...args) => {
        try {
          return await target[prop](...args);
        } catch (_) {
          console.warn(`[Mock] Using mock data for ${prop}`);
          return MOCK[mockKey] || {};
        }
      };
    }
  });
}

// Export all services
window.AdvisoryService = AdvisoryService;
window.FarmerService   = FarmerService;
window.BuyerService    = BuyerService;
window.AdminService    = AdminService;
window.CropService     = CropService;
window.AuthService     = AuthService;
window.Auth            = Auth;
window.UI              = UI;
window.MOCK            = MOCK;
window.USE_MOCK        = USE_MOCK;
window.APIError        = APIError;