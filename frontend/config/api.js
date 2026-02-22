// frontend/config/api.js

const BASE_URL = "http://127.0.0.1:8000/api/v1";
/**
 * Get JWT token from localStorage
 */
function getToken() {
    return localStorage.getItem("access_token");
}

/**
 * Generic API Request Handler
 */
async function apiRequest(endpoint, method = "GET", body = null) {
    const headers = {
        "Content-Type": "application/json",
    };

    const token = getToken();
    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const options = {
        method,
        headers,
    };

    if (body) {
        options.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, options);

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        return data;
    } catch (error) {
        console.error("API Error:", error.message);
        throw error;
    }
}

/**
 * Auth APIs
 */
export const AuthAPI = {
    register: (payload) =>
        apiRequest("/auth/register", "POST", payload),

    login: (payload) =>
        apiRequest("/auth/login", "POST", payload),
};

/**
 * Farmer APIs
 */
export const FarmerAPI = {
    analyzeAdvisory: (payload) =>
        apiRequest("/advisory/analyze", "POST", payload),

    addField: (payload) =>
        apiRequest("/farmer/fields", "POST", payload),

    getProfile: () =>
        apiRequest("/farmer/profile"),
};

/**
 * Buyer APIs
 */
export const BuyerAPI = {
    getListings: () =>
        apiRequest("/buyers/listings"),

    submitBid: (payload) =>
        apiRequest("/buyers/bid", "POST", payload),
};

/**
 * Admin APIs
 */
export const AdminAPI = {
    overview: () =>
        apiRequest("/admin/analytics/overview"),

    co2Analytics: () =>
        apiRequest("/admin/analytics/co2"),
};