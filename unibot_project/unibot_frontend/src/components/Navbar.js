import { useState, useEffect } from "react";
import { NavLink, Link, useNavigate, useLocation } from "react-router-dom";

export default function Navbar() {
  const base = "px-3 py-2 rounded-lg hover:bg-white/10 transition";
  const active = "bg-white/20 text-white";
  const token = localStorage.getItem("token");
  const navigate = useNavigate();
  const location = useLocation();

  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 30);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
    window.location.reload();
  };

  const isLanding = location.pathname === "/";

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 font-cairo ${
        scrolled
          ? "bg-blue-600/70 backdrop-blur-md shadow-md"
          : isLanding
          ? "bg-blue-500/40 backdrop-blur-sm"
          : "bg-white/80 backdrop-blur-md shadow-sm"
      }`}
    >
      <div
        className={`max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between ${
          isLanding ? "text-white" : "text-gray-800"
        }`}
      >
        <Link
          to="/"
          className={`text-xl font-bold ${
            isLanding ? "text-white" : "text-blue-800"
          } drop-shadow-md hover:opacity-90 transition`}
        >
          Unibot 🤖
        </Link>

        <nav className="flex gap-1">
          <NavLink
            to="/"
            className={({ isActive }) =>
              `${base} ${isActive ? active : ""}`
            }
          >
            الرئيسية
          </NavLink>
          <NavLink
            to="/events"
            className={({ isActive }) =>
              `${base} ${isActive ? active : ""}`
            }
          >
            الأحداث
          </NavLink>
          <NavLink
            to="/chat"
            className={({ isActive }) =>
              `${base} ${isActive ? active : ""}`
            }
          >
            المحادثة
          </NavLink>
          <NavLink
            to="/profile"
            className={({ isActive }) =>
              `${base} ${isActive ? active : ""}`
            }
          >
            الملف الشخصي
          </NavLink>
        </nav>

        {token ? (
          <button
            onClick={handleLogout}
            className={`px-3 py-2 rounded-lg ${
              isLanding
                ? "bg-red-500/80 hover:bg-red-600/90 text-white"
                : "bg-red-600 hover:bg-red-700 text-white"
            } transition`}
          >
            خروج
          </button>
        ) : (
          <Link
            to="/login"
            className={`px-3 py-2 rounded-lg ${
              isLanding
                ? "bg-white/20 text-white hover:bg-white/30"
                : "bg-blue-700 text-white hover:bg-blue-800"
            } transition`}
          >
            دخول
          </Link>
        )}
      </div>
    </header>
  );
}
