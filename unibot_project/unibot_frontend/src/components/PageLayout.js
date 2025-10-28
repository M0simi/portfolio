import React from "react";

export default function PageLayout({ children }) {
  return (
    <section dir="rtl" className="min-h-screen bg-gray-50 flex flex-col">
      <main className="flex-1 flex flex-col items-center justify-center px-4 py-12">
        <div className="w-full max-w-3xl bg-white rounded-2xl shadow-sm border p-8">
          {children}
        </div>
      </main>

      <footer className="py-6 text-center text-sm text-gray-500">
        <span className="inline-flex items-center gap-1">
          ❤️ واجهة مبنية بحب — Unibot 2025 ©
        </span>
      </footer>
    </section>
  );
}

