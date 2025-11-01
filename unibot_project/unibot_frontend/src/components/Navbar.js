import { useState, useEffect } from "react";
import { NavLink, Link, useNavigate, useLocation } from "react-router-dom";
import logo from "../assets/vector/default-monochrome-white.svg";

export default function Navbar() {
  const base =
    "px-3 py-2 rounded-lg transition hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/20";
  const active = "bg-white/20 text-white";

  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token");

  const [scrolled, setScrolled] = useState(false);
  const isLanding = location.pathname === "/";

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 30);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  // الحالة اللونية المطلوبة:
  // - أعلى اللاندنق (مو متحرك): شفاف خفيف + نص أبيض
  // - إذا نزل أو في أي صفحة ثانية: أزرق فاتح ثابت + نص أبيض
  const headerBg =
    isLanding && !scrolled
      ? "bg-white/0 backdrop-blur-[1px]" // تقريبًا شفاف فوق الهيرو
      : "bg-blue-500/80 backdrop-blur-md shadow-md"; // أزرق خفيف فاتح عند السكrol وباقي الصفحات

  const textColor = isLanding && !scrolled ? "text-white" : "text-white";

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
    // نعيد تهيئة الصفحة لو تحب
    // window.location.reload();
  };

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 font-cairo ${headerBg}`}>
      <div className={`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between ${textColor}`}>
        {/* الشعار */}
        <Link to="/" className="flex items-center">
          <div
            className={[
              "rounded-xl p-1.5",
              isLanding && !scrolled ? "bg-white/15" : "bg-white/10",
              "ring-1 ring-white/10 shadow-sm"
            ].join(" ")}
          >
            <img src={logo} alt="Unibot logo" className="h-8 w-auto object-contain md:h-9" />
          </div>
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
            تسجيل الدخول
          </Link>
        )}
      </div>
    </header>
  );
}
