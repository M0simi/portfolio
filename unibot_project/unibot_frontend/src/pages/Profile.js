import React, { useEffect, useState } from "react";
import axios from "axios";

const Profile = () => {
  const [profile, setProfile] = useState({ name: "", email: "", role: "" });
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  // ✅ جلب بيانات المستخدم بعد تسجيل الدخول
  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) return;

    axios
      .get("https://api.unibot.foo/api/prfile", {
        headers: { Authorization: `Token ${token}` },
      })
      .then((res) => setProfile(res.data))
      .catch(() => setMessage("حدث خطأ أثناء جلب البيانات."))
      .finally(() => setLoading(false));
  }, []);

  // ✅ حفظ التعديلات
  const handleSave = () => {
    const token = localStorage.getItem("token");
    axios
      .put("http://127.0.0.1:8000/api/profile/", profile, {
        headers: { Authorization: `Token ${token}` },
      })
      .then((res) => {
        setProfile(res.data.user);
        setMessage("✅ تم حفظ التغييرات بنجاح");
      })
      .catch(() => setMessage("❌ فشل تحديث البيانات"));
  };

  if (loading) return <p className="text-center mt-10">جاري تحميل البيانات...</p>;

  return (
    <div className="max-w-3xl mx-auto bg-white shadow rounded-lg p-8 mt-10 font-cairo">
      <h2 className="text-2xl font-bold text-center mb-6">ملفي الشخصي</h2>
      {message && (
        <p className="text-center mb-4 text-sm text-blue-600">{message}</p>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-gray-700 mb-2">الاسم</label>
          <input
            type="text"
            value={profile.name}
            onChange={(e) => setProfile({ ...profile, name: e.target.value })}
            className="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <div>
          <label className="block text-gray-700 mb-2">البريد الإلكتروني</label>
          <input
            type="email"
            value={profile.email}
            disabled
            className="w-full bg-gray-100 border rounded-lg px-3 py-2 text-gray-500 cursor-not-allowed"
          />
        </div>
               <div>
          <label className="block text-gray-700 mb-2">الدور</label>
          <input
            type="text"
            value="طالب"
            readOnly
            className="w-full border rounded-lg px-3 py-2 bg-gray-100 cursor-not-allowed"/>
        </div>
      </div>

      <div className="flex justify-end mt-8 space-x-4 space-x-reverse">
        <button
          onClick={handleSave}
          className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          حفظ
        </button>
      </div>
    </div>
  );
};

export default Profile;

