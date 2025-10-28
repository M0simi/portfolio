import axios from "axios";

export const sendToGemini = async (prompt) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/api/ai/general/", { prompt });
    return response.data.result;
  } catch (error) {
    console.error("❌ خطأ في الاتصال بـ Gemini API:", error);
    return "حدث خطأ أثناء الاتصال بالخادم. حاول مرة أخرى لاحقًا.";
  }
};

