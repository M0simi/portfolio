import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Calendar, MapPin, X } from 'lucide-react';

const Sidebar = ({ sidebarOpen, setSidebarOpen }) => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await axios.get('events/');
        setEvents(response.data);
      } catch (err) {
        console.error('خطأ في جلب الأحداث:', err);
      }
      setLoading(false);
    };
    fetchEvents();
  }, []);

  return (
    <>
      {sidebarOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden" onClick={() => setSidebarOpen(false)} />
      )}
      <aside className={`fixed inset-y-0 right-0 z-50 w-80 bg-white shadow-2xl transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:w-64 overflow-y-auto ${
        sidebarOpen ? 'translate-x-0' : 'translate-x-full'
      }`}>
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900 font-cairo">الأحداث القادمة</h2>
            <button onClick={() => setSidebarOpen(false)} className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition">
              <X className="h-5 w-5 text-gray-500" />
            </button>
          </div>
        </div>
        <div className="p-6 space-y-4">
          {loading ? (
            <div className="flex justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          ) : events.length === 0 ? (
            <div className="text-center py-8">
              <Calendar className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-gray-500 font-cairo">لا توجد أحداث حاليًا</p>
            </div>
          ) : (
            events.map((event) => (
              <div key={event.id} className="bg-white border border-gray-200 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow">
                <h3 className="font-semibold text-gray-900 mb-2 font-cairo truncate">{event.title}</h3>
                <div className="flex items-center space-x-2 space-x-reverse text-sm text-gray-600 mb-2">
                  <Calendar className="h-4 w-4" />
                  <span className="font-cairo">{new Date(event.start_date).toLocaleDateString('ar-SA')}</span>
                </div>
                {event.location && (
                  <div className="flex items-center space-x-2 space-x-reverse text-sm text-gray-600">
                    <MapPin className="h-4 w-4" />
                    <span className="font-cairo">{event.location}</span>
                  </div>
                )}
              </div>
            ))
          )}
        </div>
      </aside>
    </>
  );
};

export default Sidebar;
