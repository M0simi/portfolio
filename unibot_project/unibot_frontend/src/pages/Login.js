import React, { useState } from "react";
import axios from "axios";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { LogIn, Mail, Lock } from "lucide-react";

const Login = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();
  // لو جاي من Protected (مثلاً حاول يفتح /chat) بنلاقي المسار هنا
  const from = location.state?.from || "/home";

  const extractError = (err) => {
    const data = err?.response?.data;
    if (!data) return "خطأ في الاتصال بالخادم";
    if (typeof data === "string") return data;
    if (data.detail) return String(data.detail);
    if (data.error) return String(data.error);
    const firstKey = Object.keys(data)[0];
    if (firstKey) {
      const val = data[firstKey];
      if (Array.isArray(val) && val.length) return String(val[0]);
      return String(val);
    }
    return "بيانات غير صحيحة، حاول مرة أخرى";
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      // NOTE: عدّل المسار لو مختلف عندكم (مثلاً: auth/login/)
      const res = await axios.post("login/", { email, password });

      // متوقع: { token: "...", is_admin: true/false }
      const { token, is_admin } = res.data || {};
      if (!token) throw new Error("لم يصل رمز الدخول من الخادم");

      // خزّن التوكن بالطريقة المعتمدة في App
      onLogin(token);

      // خياري: خزّن is_admin لو متوفر
      if (typeof is_admin !== "undefined") {
        localStorage.setItem("is_admin", String(!!is_admin));
      }

      // رجّع المستخدم للمسار اللي كان ناوي عليه أو /home
      navigate(from, { replace: true });
    } catch (err) {
      setError(extractError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600 px-4 py-12">
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl p-8 space-y-6 animate-fade-in">
        <div className="text-center space-y-3">
          <LogIn className="mx-auto h-12 w-12 text-blue-600" />
          <h2 className="text-3xl font-bold text-gray-900 font-cairo">دخول Unibot</h2>
          <p className="text-gray-500 text-sm font-cairo">شاتبوت الجامعة الذكي</p>
          {location.state?.from && (
            <p className="text-xs text-blue-700 bg-blue-50 border border-blue-100 rounded-lg px-3 py-2 inline-block mt-2">
              تم تحويلك من <span className="font-semibold">{location.state.from}</span> — سجّل الدخول للمتابعة.
            </p>
          )}
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 font-cairo">البريد الإلكتروني</label>
            <div className="relative">
              <Mail className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 font-cairo"
                placeholder="admin@unibot.com"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="block text-sm font-medium text-gray-700 font-cairo">كلمة المرور</label>
            <div className="relative">
              <Lock className="absolute right-3 top-3 h-5 w-5 text-gray-400" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pr-10 pl-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 font-cairo"
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          {error && (
            <p className="text-red-600 text-sm text-center font-cairo p-3 bg-red-50 rounded-lg">
              {error}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 rounded-xl transition duration-200 shadow-md hover:shadow-lg font-cairo flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                جاري الدخول...
              </>
            ) : (
              <>
                <LogIn className="h-5 w-5" />
                دخول
              </>
            )}
          </button>
        </form>

        <div className="text-center text-sm text-gray-600 font-cairo">
          مستخدم جديد؟{" "}
          <Link to="/register" className="text-blue-700 hover:underline">
            إنشاء حساب
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Login;
