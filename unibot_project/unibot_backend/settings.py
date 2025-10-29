import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'jazzmin',  # Admin theme - must be before django.contrib.admin
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

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
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

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Custom user model
AUTH_USER_MODEL = 'core.CustomUser'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"

# Additional locations of static files
STATICFILES_DIRS = [
    BASE_DIR / "core" / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework
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

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Only for development!

# ===============================
# Jazzmin Admin Interface Settings
# ===============================
JAZZMIN_SETTINGS = {
    # Site branding
    "site_title": "إدارة UniBot",
    "site_header": "UniBot - لوحة التحكم",
    "site_brand": "إدارة UniBot",
    "welcome_sign": "مرحباً بك في لوحة إدارة UniBot 👋",
    
    #language rtl
    "language_rtl": True,

    # Logo configuration
    "site_logo": "core/img/unibot_logo.png",
    "login_logo": "core/img/unibot_logo.png",
    "login_logo_dark": "core/img/unibot_logo.png",
    "site_logo_classes": "img-circle",
    
    # Custom CSS
    "custom_css": "css/jazzmin_fix.css",
    "custom_js": None,
    
    # Copyright
    "copyright": "UniBot © 2025 - جميع الحقوق محفوظة",
    
    # Search
    "search_model": ["core.CustomUser", "core.FAQ", "core.Event"],
    
    # Top menu links
    "topmenu_links": [
        {"name": "الرئيسية", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "الموقع", "url": "/", "new_window": True},
    ],
    
    # User menu links
    "usermenu_links": [
        {"name": "الملف الشخصي", "url": "admin:core_customuser_changelist"},
        {"model": "auth.user"}
    ],
    
    # Show/hide UI elements
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "show_ui_builder": False,
    
    # Language and direction
    "language_chooser": False,
    
    # Model ordering
    "order_with_respect_to": [
        "core.CustomUser",
        "core.Event", 
        "core.FAQ",
        "auth.Group",
    ],
    
    # Icons for apps and models
    "icons": {
        "auth": "fas fa-shield-alt",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "core": "fas fa-robot",
        "core.CustomUser": "fas fa-user-graduate",
        "core.Event": "fas fa-calendar-check",
        "core.FAQ": "fas fa-question-circle",
    },
    
    # Default icon for apps/models
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related modal
    "related_modal_active": False,
    
    # Theme
    "theme": "cosmo",
    "dark_mode_theme": "darkly",
    
    # Change form
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
}

# Jazzmin UI Tweaks
JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-white",
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "cosmo",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}


# Media files (uploaded content like PDFs)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

