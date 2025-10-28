import React, { useState } from "react";
import axios from "axios";

export default function Chat() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    // أضف سؤال المستخدم مباشرة في المحادثة
    setMessages((prev) => [...prev, { role: "user", text: prompt }]);
    setPrompt("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");
      const response = await axios.post(
        "http://127.0.0.1:8000/api/ai/general/",
        { prompt },
        {
          headers: {
            Authorization: `Token ${token}`,
          },
        }
      );

      // أضف رد البوت
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: response.data.result || "ما قدرت أفهم سؤالك 🤖" },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "حدث خطأ في الاتصال بالخادم ⚠️" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section
      dir="rtl"
      className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-100 flex flex-col items-center py-10"
    >
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg border p-6 flex flex-col">
        <h1 className="text-2xl font-bold text-center text-blue-700 mb-4">
          🎓 UniBot - المساعد الجامعي الذكي
        </h1>

        <div className="flex-1 overflow-y-auto space-y-3 mb-4 p-3 bg-gray-50 rounded-lg border">
          {messages.length === 0 ? (
            <p className="text-gray-400 text-center mt-8">
              ابدأ بطرح سؤالك للـ UniBot 🤖
            </p>
          ) : (
            messages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-xl ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white self-end ml-auto max-w-[80%]"
                    : "bg-gray-200 text-gray-800 self-start mr-auto max-w-[80%]"
                }`}
              >
                {msg.text}
              </div>
            ))
          )}

          {loading && (
            <div className="flex justify-center mt-4">
              <div className="w-6 h-6 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
          )}
        </div>

        <form
          onSubmit={handleSend}
          className="flex items-center gap-3 border-t pt-3"
        >
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="اكتب سؤالك هنا..."
            className="flex-1 p-3 border rounded-xl outline-none focus:ring-2 focus:ring-blue-200"
          />
          <button
            type="submit"
            disabled={loading}
            className="px-5 py-3 bg-blue-700 text-white rounded-xl hover:bg-blue-800 transition disabled:opacity-50"
          >
            إرسال
          </button>
        </form>
      </div>
    </section>
  );
}

