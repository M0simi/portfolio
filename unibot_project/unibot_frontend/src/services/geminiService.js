import axios from "axios";

/* =====================================
   🌍 إعداد عنوان الـ Backend
   - محلي: http://127.0.0.1:8000/api/
   - إنتاج: https://api.unibot.foo/api/
===================================== */
const BASE_URL =
  window.location.hostname === "localhost" ||
  window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000/api/"
    : "https://api.unibot.foo/api/";

/* =====================================
   🤖 دالة إرسال السؤال إلى Gemini عبر Django
===================================== */
export const sendToGemini = async (prompt) => {
  try {
    const token = localStorage.getItem("token");

    const response = await axios.post(
      `${BASE_URL}ai/general/`,
      { prompt },
      {
        headers: {
          "Content-Type": "application/json",
          ...(token ? { Authorization: `Token ${token}` } : {}),
        },
      }
    );

    return response.data.result;
  } catch (error) {
    console.error("❌ خطأ في الاتصال بـ Gemini API:", error);

    if (error.response) {
      // خطأ من السيرفر نفسه (status 4xx أو 5xx)
      return (
        error.response.data.error ||
        "حدث خطأ من الخادم أثناء معالجة طلبك. حاول لاحقًا."
      );
    } else if (error.request) {
      // السيرفر لم يرد (timeout أو network error)
      return "تعذر الاتصال بالخادم. تأكد من اتصال الإنترنت أو حاول بعد قليل.";
    } else {
      // خطأ آخر غير متوقع
      return "حدث خطأ غير متوقع. حاول لاحقًا.";
    }
  }
};
