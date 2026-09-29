"""
Configuración principal del proyecto Club Óptica Brigantium.

Los datos privados (clave secreta, contraseña de la base de datos, correo)
NO se guardan aquí: se leen de config/local_settings.py, que no se sube a GitHub.
Copia config/local_settings.example.py como config/local_settings.py y rellénalo.
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Valores por defecto (se sobrescriben en local_settings.py)
SECRET_KEY = "cambiar-en-local-settings"
DEBUG = False
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps del proyecto
    "cuentas",    # usuarios, registro, login y roles
    "club",       # parte pública y área privada del cliente
    "campanas",   # campañas, condiciones y beneficios
    "cupones",    # cupones, QR y canjes
    "panel",      # panel del personal y métricas
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Base de datos: se define en local_settings.py (MySQL)
DATABASES = {}

# Modelo de usuario propio. IMPORTANTE: debe existir antes de la primera migración.
AUTH_USER_MODEL = "cuentas.Usuario"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "cuentas:login"
LOGIN_REDIRECT_URL = "club:inicio"
LOGOUT_REDIRECT_URL = "club:inicio"

# Idioma y zona horaria
LANGUAGE_CODE = "es-es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

# Ficheros estáticos (CSS, JS, imágenes del diseño)
STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"   # donde se recopilan al publicar

# Ficheros subidos (imágenes de campañas) y exportaciones CSV
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Correo: en local se muestran los correos en la consola en vez de enviarlos
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = "Club Óptica Brigantium <no-responder@opticabrigantium.es>"

# Cargar la configuración privada
try:
    from .local_settings import *  # noqa: F401,F403
except ImportError:
    raise ImportError(
        "Falta config/local_settings.py. Copia local_settings.example.py y rellénalo."
    )
