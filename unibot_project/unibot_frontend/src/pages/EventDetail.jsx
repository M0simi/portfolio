// unibot_frontend/src/pages/EventDetail.jsx
import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

export default function EventDetail()
{
  const { slug } = useParams(); // slug من الرابط
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() =>
  {
    axios
      .get(`/events/${slug}/`) // ✅ نسبي لأن baseURL مضبوط في App.js
      .then((res) =>
      {
        setEvent(res.data);
        setLoading(false);
      })
      .catch((err) =>
      {
        console.error("خطأ في جلب تفاصيل الحدث:", err);
        setLoading(false);
      });
  }, [slug]);

  if (loading)
  {
    return (
      <div className="flex items-center justify-center min-h-screen font-cairo text-gray-700">
        جاري تحميل تفاصيل الحدث...
      </div>
    );
  }

  if (!event)
  {
    return (
      <div className="text-center mt-10 font-cairo">
        <p className="text-gray-600 mb-4">❌ لم يتم العثور على الحدث.</p>
        <Link to="/events" className="text-blue-600 underline hover:text-blue-800">
          العودة إلى الأحداث
        </Link>
      </div>
    );
  }

  const startText = new Date(event.start_date).toLocaleDateString("ar-SA");
  const endText = event.end_date ? new Date(event.end_date).toLocaleDateString("ar-SA") : null;

  return (
    <section
      dir="rtl"
      className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center py-10 px-4 font-cairo"
    >
      <div className="max-w-3xl bg-white rounded-2xl shadow-md p-6 w-full">
        {/* صورة الحدث */}
        {event.image_url && (
          <img
            src={event.image_url}
            alt={event.title}
            className="rounded-xl w-full h-64 object-cover mb-4 shadow"
          />
        )}

        {/* العنوان */}
        <h1 className="text-2xl font-bold text-blue-800 mb-2">{event.title}</h1>

        {/* التاريخ والموقع */}
        <p className="text-gray-600 mb-1">
          {endText ? (
            <>📅 من {startText} إلى {endText}</>
          ) : (
            <>📅 تاريخ البدء: {startText}</>
          )}
        </p>

        {event.location && <p className="text-gray-500 mb-4">📍 {event.location}</p>}

        {/* الوصف */}
        <p className="leading-relaxed text-gray-800 whitespace-pre-line mb-6">
          {event.description || "لا توجد تفاصيل مضافة لهذا الحدث."}
        </p>

        {/* زر العودة */}
        <Link
          to="/events"
          className="inline-block bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition"
        >
          ← العودة إلى قائمة الأحداث
        </Link>
      </div>
    </section>
  );
}
