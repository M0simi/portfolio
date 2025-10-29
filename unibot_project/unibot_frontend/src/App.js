import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from "react-router-dom";
import axios from "axios";

import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Landing from "./pages/Landing";
import Events from "./pages/Events";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";

// إعداد Axios
axios.defaults.baseURL = "https://unibot.foo/api/";
axios.defaults.headers.post["Content-Type"] = "application/json";

// حارس المسارات المحمية: يرسل المستخدم إلى /login إن لم يكن مسجلاً الدخول
function Protected({ children, token }) {
  const location = useLocation();
  return token ? children : <Navigate to="/login" replace state={{ from: location.pathname }} />;
}

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
        <Navbar />
        <main className="flex-1 w-full bg-gradient-to-b from-blue-100 to-blue-200">
          <Routes>
            {/* صفحات عامة */}
            <Route path="/" element={<Landing />} />
            <Route path="/events" element={<Events />} />

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

