import { NavLink, Link } from "react-router-dom";
import logo from "../assets/vector/default-monochrome-white.svg";

export default function Navbar() {
  const base =
    "px-3 py-2 rounded-lg transition hover:bg-white/10 focus:outline-none focus:ring-2 focus:ring-white/20";
  const active = "bg-white/20 text-white";

  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.assign("/");
  };

  return (
    <header className="sticky top-0 z-50 bg-blue-600/90 backdrop-blur-md shadow-md font-cairo">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between text-white">
        {/* الشعار */}
        <Link to="/" className="flex items-center">
          <div className="rounded-xl p-1.5 bg-white/15 ring-1 ring-white/10 shadow-sm">
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
            className="px-3 py-2 rounded-lg bg-red-600 hover:bg-red-700 transition"
          >
            خروج
          </button>
        ) : (
          <Link
            to="/login"
            className="px-3 py-2 rounded-lg bg-blue-800 hover:bg-blue-900 transition"
          >
            تسجيل الدخول
          </Link>
        )}
      </div>
    </header>
  );
}
