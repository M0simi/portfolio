import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';

i18n.use(initReactI18next).init({
  resources: {
    ar: {
      translation: {
        title: 'Unibot - شاتبوت الجامعة',
        chatPlaceholder: 'اكتب سؤالك...',
        error: 'خطأ في الاتصال بالخادم.',
        events: 'الأحداث القادمة',
        noEvents: 'لا أحداث حاليًا.',
        loginEmail: 'البريد الإلكتروني',
        loginPassword: 'كلمة المرور',
        loginButton: 'دخول',
        logout: 'خروج',
        loginTitle: 'تسجيل الدخول'  // إضافة جديدة (New key)
      }
    },
    en: {
      translation: {
        title: 'Unibot - University Chatbot',
        chatPlaceholder: 'Type your question...',
        error: 'Server connection error.',
        events: 'Upcoming Events',
        noEvents: 'No events currently.',
        loginEmail: 'Email',
        loginPassword: 'Password',
        loginButton: 'Login',
        logout: 'Logout',
        loginTitle: 'Sign In'  // إضافة جديدة (New key)
      }
    }
  },
  lng: 'ar',
  fallbackLng: 'ar',
  interpolation: { escapeValue: false }
});

export default i18n;
