// API wrappers الكاملة (Full API service wrappers - uses backend services indirectly)
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',  // Backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// إضافة التوكن تلقائيًا (Auto add token)
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const api = {
  login: (email, password) => apiClient.post('auth/login/', { email, password }),  // تسجيل الدخول (Login)
  getFaqs: (query = '', category_id = '') => apiClient.get('faqs/', { params: { query, category_id } }),  // قائمة FAQs
  createFaq: (data) => apiClient.post('faqs/', data),  // إنشاء FAQ
  updateFaq: (data) => apiClient.put('faqs/', data),  // تحديث
  deleteFaq: (id) => apiClient.delete('faqs/', { data: { id } }),  // حذف
  getEvents: (from = '', to = '') => apiClient.get('events/', { params: { from, to } }),  // أحداث
  createEvent: (data) => apiClient.post('events/', data),  // إنشاء حدث
  search: (query, top_k = 5) => apiClient.post('search/', { query, top_k }),  // بحث
  submitFeedback: (data) => apiClient.post('feedback/', data),  // تعليق
  getFeedback: (faq_id) => apiClient.get('feedback/', { params: { faq_id } }),  // قائمة تعليقات
  toggleFavorite: (faq_id) => apiClient.post('favorites/', { faq_id }),  // تبديل مفضلة
  getFavorites: () => apiClient.get('favorites/'),  // قائمة مفضلة
};

export default apiClient;
