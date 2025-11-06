import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";

const SA_UNIVERSITIES = [
  "جامعة الملك سعود",
  "جامعة الإمام محمد بن سعود الإسلامية",
  "جامعة الملك عبدالعزيز",
  "جامعة الأميرة نورة بنت عبدالرحمن",
  "جامعة الملك فهد للبترول والمعادن",
  "جامعة الملك خالد",
  "جامعة الأمير سطّام بن عبدالعزيز",
  "جامعة القصيم",
  "جامعة الطائف",
  "جامعة الملك فيصل",
  "جامعة جدة",
  "جامعة حائل",
  "جامعة تبوك",
  "جامعة جازان",
  "جامعة نجران",
  "جامعة بيشة",
];

export default function SignUp() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    university: "",
  });

  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((f) => ({ ...f, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg("");

    try {
      const response = await axios.post("https://api.unibot.foo/api/register", form);

      if (response.status === 201 || response.status === 200) {
        alert("تم إنشاء الحساب بنجاح ✅");
        navigate("/profile"); // تحويل تلقائي لصفحة الملف الشخصي
      } else {
        setErrorMsg("حدث خطأ أثناء إنشاء الحساب. حاول مرة أخرى.");
      }
    } catch (error) {
      console.error("Registration error:", error);
      setErrorMsg("البريد مستخدم من قبل أو هناك خطأ في الخادم.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section dir="rtl" className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-1 flex items-start justify-center px-4">
        <form
          onSubmit={handleSubmit}
          className="w-full max-w-md bg-white rounded-2xl shadow-sm border mt-16 p-6"
        >
          <h1 className="text-2xl font-extrabold text-gray-900 mb-6">
            إنشاء حساب جديد
          </h1>

          {errorMsg && (
            <p className="text-red-600 bg-red-50 p-2 rounded-lg mb-3 text-sm text-center">
              {errorMsg}
            </p>
          )}

          {/* الاسم */}
          <input
            type="text"
            name="name"
            placeholder="الاسم الكامل"
            value={form.name}
            onChange={handleChange}
            className="w-full mb-3 rounded-xl border border-gray-300 bg-gray-50 focus:bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-200"
            required
          />

          {/* البريد */}
          <input
            type="email"
            name="email"
            placeholder="البريد الإلكتروني"
            value={form.email}
            onChange={handleChange}
            className="w-full mb-3 rounded-xl border border-gray-300 bg-gray-50 focus:bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-200"
            required
          />

          {/* كلمة المرور */}
          <input
            type="password"
            name="password"
            placeholder="كلمة المرور"
            value={form.password}
            onChange={handleChange}
            className="w-full mb-3 rounded-xl border border-gray-300 bg-gray-50 focus:bg-white px-4 py-3 outline-none focus:ring-2 focus:ring-blue-200"
            required
          />

          {/* الجامعة */}
          <label className="block text-sm text-gray-700 mb-1">
            الجامعة أو الكلية
          </label>
          <select
            name="university"
            value={form.university}
            onChange={handleChange}
            className="w-full mb-5 rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 outline-none focus:ring-2 focus:ring-blue-200"
            required
          >
            <option value="" disabled>
              اختر الجامعة
            </option>
            {SA_UNIVERSITIES.map((u) => (
              <option key={u} value={u}>
                {u}
              </option>
            ))}
          </select>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-xl bg-blue-700 text-white py-3 font-semibold hover:bg-blue-800 disabled:opacity-50"
          >
            {loading ? "جاري الإنشاء..." : "إنشاء الحساب"}
          </button>

          <p className="text-sm text-gray-600 mt-4 text-center">
            عندك حساب؟{" "}
            <Link to="/login" className="text-blue-700 hover:underline">
              اضغط هنا لتسجيل الدخول
            </Link>
          </p>
        </form>
      </main>

      <footer className="py-6 text-center text-sm text-gray-500">
        <span className="inline-flex items-center gap-1">
          ❤️ واجهة مبنية بحب — Unibot 2025 ©
        </span>
      </footer>
    </section>
  );
}

