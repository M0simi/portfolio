import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";
import axios from "axios";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Landing from "./pages/Landing";
import Events from "./pages/Events";
import EventDetail from "./pages/EventDetail"; // ✅ جديد
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";

/* ================================
   🔧 إعداد Axios (اتصال الباك إند)
================================ */
axios.defaults.baseURL = "https://api.unibot.foo/api"; // ✅ بدون "/" في النهاية
axios.defaults.headers.common["Content-Type"] = "application/json";

// 🎫 إضافة التوكن تلقائيًا مع كل طلب
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

/* ================================
   🛡️ حارس المسارات المحمية
================================ */
function Protected({ children, token }) {
  const location = useLocation();
  return token ? (
    children
  ) : (
    <Navigate to="/login" replace state={{ from: location.pathname }} />
  );
}

/* ================================
   🧠 المكون الرئيسي للتطبيق
================================ */
export default function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      axios.defaults.headers.common["Authorization"] = `Token ${token}`;
    } else {
      delete axios.defaults.headers.common["Authorization"];
    }
    setLoading(false);
  }, [token]);

  const handleLogin = (newToken) => {
    setToken(newToken);
    localStorage.setItem("token", newToken);
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem("token");
    delete axios.defaults.headers.common["Authorization"];
    window.location.assign("/");
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-lg font-medium text-gray-700 font-cairo">جاري التحميل...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-gray-50 font-cairo">
        <Navbar onLogout={handleLogout} />
        <main className="flex-1 w-full bg-gradient-to-b from-blue-100 to-blue-200">
          <Routes>
            {/* صفحات عامة */}
            <Route path="/" element={<Landing />} />
            <Route path="/events" element={<Events />} />
            <Route path="/events/:slug" element={<EventDetail />} /> {/* ✅ جديد */}

            {/* مصادقة */}
            <Route
              path="/login"
              element={!token ? <Login onLogin={handleLogin} /> : <Navigate to="/" replace />}
            />
            <Route
              path="/register"
              element={!token ? <Register /> : <Navigate to="/" replace />}
            />

            {/* صفحات محمية */}
            <Route
              path="/chat"
              element={
                <Protected token={token}>
                  <Chat />
                </Protected>
              }
            />
            <Route
              path="/profile"
              element={
                <Protected token={token}>
                  <Profile />
                </Protected>
              }
            />

            {/* أي مسار غير معروف */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}
