import React, { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

export default function Events()
{
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() =>
  {
    setLoading(true);
    axios
      .get(`/events/?status=${filter}`)
      .then((res) =>
      {
        setEvents(res.data);
        setLoading(false);
      })
      .catch((err) =>
      {
        console.error("خطأ في جلب الأحداث:", err);
        setLoading(false);
      });
  }, [filter]);

  if (loading)
  {
    return (
      <div className="flex justify-center items-center min-h-screen font-cairo text-gray-700">
        جاري تحميل الأحداث...
      </div>
    );
  }

  return (
    <section className="font-cairo py-10 bg-gray-50 min-h-screen" dir="rtl">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-extrabold text-blue-800">
          الأحداث الجامعية
        </h1>
        <p className="text-gray-600 mt-2">
          هنا تلاقي أحدث الفعاليات وورش العمل
        </p>
      </div>

      {/* 🔹 الفلاتر */}
      <div className="flex justify-center gap-3 mb-8">
        {["all", "upcoming", "past"].map((status) => (
          <button
            key={status}
            onClick={() => setFilter(status)}
            className={`px-4 py-2 rounded-lg font-medium ${
              filter === status
                ? "bg-blue-700 text-white"
                : "bg-white border border-blue-300 text-blue-700"
            }`}
          >
            {status === "all"
              ? "الكل"
              : status === "upcoming"
              ? "القادمة"
              : "المنتهية"}
          </button>
        ))}
      </div>

      {events.length === 0 ? (
        <p className="text-center text-gray-500">لا توجد فعاليات حالياً.</p>
      ) : (
        <div className="max-w-6xl mx-auto grid gap-6 sm:grid-cols-2 md:grid-cols-3">
          {events.map((event) => (
            <Link
              to={`/events/${event.slug}`}
              key={event.id}
              className="bg-white rounded-2xl shadow-md p-5 border hover:shadow-lg transition block"
            >
              {event.image_url && (
                <img
                  src={event.image_url}
                  alt={event.title}
                  className="w-full h-40 object-cover rounded-lg mb-3"
                />
              )}
              <h3 className="text-lg font-semibold text-gray-800 mb-2">
                {event.title}
              </h3>
              {event.location && (
                <p className="text-sm text-gray-600 mb-3">{event.location}</p>
              )}
              <p className="text-sm text-gray-500">
                {new Date(event.start_date).toLocaleDateString("ar-SA")}
              </p>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}
