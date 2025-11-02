import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Events() {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  // جلب الأحداث من API
  useEffect(() => {
    axios
      .get("https://api.unibot.foo/api/events")
      .then((res) => {
        setEvents(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("خطأ في جلب الأحداث:", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen font-cairo text-gray-700">
        جاري تحميل الأحداث...
      </div>
    );
  }

  return (
    <section className="font-cairo py-10 bg-gray-50 min-h-screen">
      <div className="text-center mb-8">
        <h1 className="text-3xl font-extrabold text-blue-800">
          الاحداث الجامعية
        </h1>
        <p className="text-gray-600 mt-2">
          هنا تلاقي أحدث الفعاليات وورش العمل
        </p>
      </div>

      {events.length === 0 ? (
        <p className="text-center text-gray-500">لا توجد فعاليات حالياً.</p>
      ) : (
        <div className="max-w-4xl mx-auto grid gap-4 sm:grid-cols-2 md:grid-cols-3">
          {events.map((event) => (
            <div
              key={event.id}
              className="bg-white rounded-2xl shadow-md p-5 border hover:shadow-lg transition"
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
              <p className="text-sm text-gray-600 mb-3">{event.location}</p>
              <p className="text-sm text-gray-500">
                {new Date(event.start_date).toLocaleDateString("ar-SA")}
              </p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

