// 🔧 Full API service wrapper for UniBot backend
import axios from "axios";

/* =====================================
   🌍 Backend Base URL Configuration
   - Local: http://127.0.0.1:8000/api/
   - Production: https://api.unibot.foo/api/
===================================== */
const apiClient = axios.create({
  baseURL:
    window.location.hostname === "localhost" ||
    window.location.hostname === "127.0.0.1"
      ? "http://127.0.0.1:8000/api/"
      : "https://api.unibot.foo/api/",
  headers: {
    "Content-Type": "application/json",
  },
});

/* =====================================
   🎫 Automatically attach Token to headers
===================================== */
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

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
  search: (query, top_k = 5) =>
    apiClient.post("search/", { query, top_k }),
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
