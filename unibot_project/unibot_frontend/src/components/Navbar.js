import { NavLink, Link, useNavigate, useLocation } from "react-router-dom";
import logo from "../assets/vector/default-monochrome-white.svg";

export default function Navbar() {
  const base = "px-3 py-2 rounded-lg hover:bg-white/10 transition";
  const active = "bg-white/20 text-white";
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
    window.location.reload();
  };

  // ⬅⬅ هنا ثبّتناه خلاص
  const headerBg = "bg-blue-500/80 backdrop-blur-md shadow-md";
  const textColor = "text-white";

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 font-cairo ${headerBg}`}
    >
      <div
        className={`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between ${textColor}`}
      >
        {/* اللوقو */}
        <Link to="/" className="flex items-center">
          <div className="rounded-xl p-1.5 bg-white/10 ring-1 ring-white/10 shadow-sm">
            <img
              src={logo}
              alt="Unibot logo"
              className="h-8 w-auto object-contain md:h-9"
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
            className="px-3 py-2 rounded-lg bg-red-500/90 hover:bg-red-600 text-white transition"
          >
            خروج
          </button>
        ) : (
          <Link
            to="/login"
            className="px-3 py-2 rounded-lg bg-white/20 text-white hover:bg-white/30 transition"
          >
            تسجيل الدخول
          </Link>
        )}
      </div>
    </header>
  );
}
