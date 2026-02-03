// 🔧 Full API service wrapper for UniBot backend (CRA)
// Uses REACT_APP_API_URL from Render env variables

import axios from "axios";

/* =====================================
   🌍 Backend Base URL Configuration
   - Local example:  http://127.0.0.1:8000
   - Production:     https://portfolio-1-tk8x.onrender.com
   NOTE: We always read from REACT_APP_API_URL
===================================== */

const rawBase = (process.env.REACT_APP_API_URL || "").trim();

// Normalize: remove trailing slashes
const normalizedBase = rawBase.replace(/\/+$/, "");

// Final API base (your endpoints in this file are like "login/", "search/", etc.)
const API_BASE_URL = normalizedBase ? `${normalizedBase}/api/` : "";

// Create axios client
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  // optional: enable sending cookies if you ever use session auth
  // withCredentials: true,
});

/* =====================================
   🧯 Helpful guard: if API url missing, log it clearly
===================================== */
if (!API_BASE_URL) {
  // This won't break the app; just tells you why requests won't fire
  // (CRA injects env vars at build time, so redeploy after setting env)
  // eslint-disable-next-line no-console
  console.warn(
    "REACT_APP_API_URL is missing. Set it in Render and redeploy the frontend."
  );
}

/* =====================================
   🎫 Automatically attach Token to headers
===================================== */
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

/* =====================================
   📦 API Endpoints Wrappers
===================================== */
export const api = {
  // Authentication
  login: (email, password) => apiClient.post("login/", { email, password }),
  register: (data) => apiClient.post("register/", data),

  // Events
  getEvents: (from = "", to = "") =>
    apiClient.get("events/", { params: { from, to } }),

  // AI Search / Chat
  search: (query, top_k = 5) => apiClient.post("search/", { query, top_k }),
  aiGeneral: (prompt) => apiClient.post("ai/general/", { prompt }),

  // Feedback and Favorites
  submitFeedback: (data) => apiClient.post("feedback/", data),
  getFeedback: (faq_id) => apiClient.get("feedback/", { params: { faq_id } }),
  toggleFavorite: (faq_id) => apiClient.post("favorites/", { faq_id }),
  getFavorites: () => apiClient.get("favorites/"),

  // FAQ management
  getFaqs: (query = "", category_id = "") =>
    apiClient.get("faqs/", { params: { query, category_id } }),
  createFaq: (data) => apiClient.post("faqs/", data),
  updateFaq: (data) => apiClient.put("faqs/", data),
  deleteFaq: (id) => apiClient.delete("faqs/", { data: { id } }),

  // Profile
  getProfile: () => apiClient.get("profile/"),
  updateProfile: (data) => apiClient.put("profile/", data),
};

export default apiClient;
