import { useState, useEffect } from "react";
import { NavLink, Link, useNavigate, useLocation } from "react-router-dom";
// ✨ مسار اللوقو الجديد
import logo from "../assets/logo.png";

export default function Navbar() {
  const base = "px-3 py-2 rounded-lg hover:bg-white/10 transition";
  const active = "bg-white/20 text-white";
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  const location = useLocation();

  const [scrolled, setScrolled] = useState(false);
  const isLanding = location.pathname === "/";

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 30);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
    window.location.reload();
  };

  // ألوان الخلفية حسب الحالة (صفحة اللاندنق/السكرول)
  const headerBg = scrolled
    ? "bg-blue-600/70 backdrop-blur-md shadow-md"
    : isLanding
    ? "bg-blue-500/40 backdrop-blur-sm"
    : "bg-white/80 backdrop-blur-md shadow-sm";

  const textColor = isLanding && !scrolled ? "text-white" : "text-gray-800";
  const brandTextColor = isLanding && !scrolled ? "text-white" : "text-blue-800";

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 font-cairo ${headerBg}`}>
      <div className={`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between ${textColor}`}>
        {/* اللوقو + اسم الموقع */}
        <Link to="/" className="flex items-center gap-2 hover:opacity-90 transition">
          <img
            src={logo}
            alt="Unibot logo"
            className="h-8 w-auto object-contain md:h-9"
            // لو كان اللوقو غامق وحاب تفتحه فوق الخلفية الزرقاء:
            // style={{ filter: isLanding && !scrolled ? "brightness(100%)" : "none" }}
          />
          <span className={`text-xl font-bold drop-shadow-md ${brandTextColor}`}>Unibot</span>
        </Link>

        {/* الروابط */}
        <nav className="flex gap-1">
          <NavLink to="/" className={({ isActive }) => `${base} ${isActive ? active : ""}`}>
            الرئيسية
          </NavLink>
          <NavLink to="/events" className={({ isActive }) => `${base} ${isActive ? active : ""}`}>
            الأحداث
          </NavLink>
          <NavLink to="/chat" className={({ isActive }) => `${base} ${isActive ? active : ""}`}>
            المحادثة
          </NavLink>
          <NavLink to="/profile" className={({ isActive }) => `${base} ${isActive ? active : ""}`}>
            الملف الشخصي
          </NavLink>
        </nav>

        {/* زر الدخول/الخروج */}
        {token ? (
          <button
            onClick={handleLogout}
            className={`px-3 py-2 rounded-lg transition ${
              isLanding && !scrolled
                ? "bg-red-500/80 hover:bg-red-600/90 text-white"
                : "bg-red-600 hover:bg-red-700 text-white"
            }`}
          >
            خروج
          </button>
        ) : (
          <Link
            to="/login"
            className={`px-3 py-2 rounded-lg transition ${
              isLanding && !scrolled
                ? "bg-white/20 text-white hover:bg-white/30"
                : "bg-blue-700 text-white hover:bg-blue-800"
            }`}
          >
            تسجيل دخول
          </Link>
        )}
      </div>
    </header>
  );
}
