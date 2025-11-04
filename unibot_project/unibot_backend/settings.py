import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Security & Debug Settings
# ==========================
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    "api.unibot.foo",
    "unibot.foo",
    "portfolio-1-ppb8.onrender.com",
    "www.unibot.foo",
    "localhost",
    "127.0.0.1"
]

# ==========================
# Installed Apps
# ==========================
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'core',
]

# ✅ Cloudinary (يُفعَّل تلقائياً إذا المفاتيح موجودة)
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')  # الشكل المفضّل: cloudinary://<api_key>:<api_secret>@<cloud_name>
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

USE_CLOUDINARY = bool(
    CLOUDINARY_URL or (CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY and CLOUDINARY_API_SECRET)
)

if USE_CLOUDINARY:
    INSTALLED_APPS += ['cloudinary', 'cloudinary_storage']

# ==========================
# Middleware
# ==========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'unibot_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'unibot_backend.wsgi.application'

# ==========================
# Database
# ==========================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==========================
# Authentication
# ==========================
AUTH_USER_MODEL = 'core.CustomUser'
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==========================
# Localization
# ==========================
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True

# ==========================
# Static & Media Files
# ==========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "core" / "static"]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# ✅ تفعيل Cloudinary لملفات الميديا (إن وُجدت المفاتيح)
if USE_CLOUDINARY:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

    # لو ما استخدمت CLOUDINARY_URL، نزود الكونفيقشن اليدوي
    if not CLOUDINARY_URL:
        CLOUDINARY_STORAGE = {
            'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
            'API_KEY': CLOUDINARY_API_KEY,
            'API_SECRET': CLOUDINARY_API_SECRET,
        }
else:
    # تخزين محلي كالمعتاد
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==========================
# REST Framework
# ==========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# ==========================
# CORS Settings
# ==========================
CORS_ALLOWED_ORIGINS = [
    "https://unibot.foo",
    "https://www.unibot.foo",
    "https://api.unibot.foo",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CSRF_TRUSTED_ORIGINS = [
    "https://unibot.foo",
    "https://www.unibot.foo",
    "https://api.unibot.foo",
]
CORS_ALLOW_CREDENTIALS = True


CORS_ALLOW_HEADERS = [
    "content-type",
    "authorization",
    "accept",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]


