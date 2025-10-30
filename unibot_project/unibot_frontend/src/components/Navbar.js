import { useState, useEffect } from "react";
import { NavLink, Link, useNavigate, useLocation } from "react-router-dom";
import logo from "../assets/logo.png"; // عدّل المسار إذا لزم

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

  // خلفية الهيدر حسب الحالة
  const headerBg = scrolled
    ? "bg-blue-600/70 backdrop-blur-md shadow-md"
    : isLanding
    ? "bg-blue-500/40 backdrop-blur-sm"
    : "bg-white/80 backdrop-blur-md shadow-sm";

  const textColor = isLanding && !scrolled ? "text-white" : "text-gray-800";

  return (
    <header className={`sticky top-0 z-50 transition-all duration-300 font-cairo ${headerBg}`}>
      <div className={`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between ${textColor}`}>
        
        {/* ==== اللوقو فقط داخل كبسولة زرقاء خفيفة ==== */}
        <Link to="/" className="flex items-center">
          <div
            className={[
              // خلفية زرقاء خفيفففة جداً مع زوايا وحجم مناسب
              "rounded-xl p-1.5",
              // درجة شفافية خفيفة جداً عشان ما تصير بلوك ثقيل
              isLanding && !scrolled ? "bg-white/15" : "bg-blue-500/10",
              // حدود خفيفة جداً تعطي تحديد بسيط
              "ring-1 ring-white/10",
              // ظلّ خفيف
              "shadow-sm"
            ].join(" ")}
          >
            <img
              src={logo}
              alt="Unibot logo"
              className="h-8 w-auto object-contain md:h-9"
              // لو اللوقو غامق على الأزرق وتبي يبان أكثر، فكّ التعليق:
              // style={{ filter: isLanding && !scrolled ? "brightness(105%)" : "none" }}
            />
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
            دخول
          </Link>
        )}
      </div>
    </header>
  );
}
