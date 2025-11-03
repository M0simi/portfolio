import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";

export default function EventDetail() {
  const { slug } = useParams();
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`https://api.unibot.foo/api/events/${slug}/`)
      .then((res) => {
        setEvent(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, [slug]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p className="text-gray-600">جاري تحميل الحدث...</p>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="text-center mt-10">
        <p>❌ لم يتم العثور على الحدث.</p>
        <Link to="/events" className="text-blue-600 underline">
          العودة للأحداث
        </Link>
      </div>
    );
  }

  return (
    <div dir="rtl" className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col items-center py-10 px-4">
      <div className="max-w-3xl bg-white rounded-2xl shadow-md p-6 w-full">
        {event.image_url && (
          <img
            src={event.image_url}
            alt={event.title}
            className="rounded-xl w-full h-64 object-cover mb-4 shadow"
          />
        )}
        <h1 className="text-2xl font-bold text-blue-800 mb-2">{event.title}</h1>
        <p className="text-gray-600 mb-2">
          📅 من {new Date(event.start_date).toLocaleDateString("ar-SA")} إلى{" "}
          {new Date(event.end_date).toLocaleDateString("ar-SA")}
        </p>
        {event.location && <p className="text-gray-500 mb-4">📍 {event.location}</p>}
        <p className="leading-relaxed text-gray-800 whitespace-pre-line">{event.description}</p>
        <Link
          to="/events"
          className="mt-6 inline-block bg-blue-700 text-white px-4 py-2 rounded-lg hover:bg-blue-800 transition"
        >
          ← العودة إلى قائمة الأحداث
        </Link>
      </div>
    </div>
  );
}
