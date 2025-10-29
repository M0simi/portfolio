import { Link } from "react-router-dom";
import { Zap, Brain, GraduationCap } from "lucide-react";

export default function Landing() {
  return (
    <section className="flex flex-col items-center justify-center min-h-screen font-cairo text-center px-6 bg-gradient-to-b from-blue-300 via-blue-100 to-white">
      {/* العنوان */}
      <h1 className="text-5xl sm:text-6xl font-extrabold text-blue-800 mb-4 animate-fadeInUp">
        مرحباً بك في <span className="text-blue-600">Unibot</span>
      </h1>

      {/* الوصف */}
      <p className="text-gray-700 max-w-2xl mb-10 leading-relaxed animate-fadeInUp delay-200">
        Unibot هو مساعد ذكي للطلاب الجامعيين، يساعدك في طرح الأسئلة العامة
        بسرعة وسهولة. رؤيتنا جعل الوصول إلى المعلومات الجامعية أقرب لكل طالب.
      </p>

      {/* الأزرار */}
      <div className="flex flex-wrap justify-center gap-4 animate-fadeInUp delay-300">
        <Link
          to="/chat"
          className="px-7 py-3 rounded-xl bg-blue-700 text-white hover:bg-blue-800 hover:scale-105 transition transform duration-200 shadow-md"
        >
          💬 ابدأ المحادثة
        </Link>
        <Link
          to="/events"
          className="px-7 py-3 rounded-xl border border-blue-700 text-blue-700 hover:bg-blue-50 hover:scale-105 transition transform duration-200"
        >
          📅 الأحداث
        </Link>
      </div>

      {/* المميزات */}
      <div className="flex flex-wrap justify-center gap-10 mt-16 text-gray-700 animate-fadeInUp delay-500">
        <div className="flex flex-col items-center">
          <Zap className="w-8 h-8 text-blue-600 mb-2" />
          <p className="font-medium">سرعة في الإجابة</p>
        </div>
        <div className="flex flex-col items-center">
          <Brain className="w-8 h-8 text-blue-600 mb-2" />
          <p className="font-medium">ذكاء وسهولة استخدام</p>
        </div>
        <div className="flex flex-col items-center">
          <GraduationCap className="w-8 h-8 text-blue-600 mb-2" />
          <p className="font-medium">مصمم للطلاب الجامعيين</p>
        </div>
      </div>

      {/* أنيميشن Tailwind مخصصة */}
      <style>{`
        @keyframes fadeInUp {
          0% { opacity: 0; transform: translateY(20px); }
          100% { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeInUp {
          animation: fadeInUp 0.8s ease forwards;
        }
        .delay-200 { animation-delay: 0.2s; }
        .delay-300 { animation-delay: 0.3s; }
        .delay-500 { animation-delay: 0.5s; }
        .delay-700 { animation-delay: 0.7s; }
      `}</style>
    </section>
  );
}
