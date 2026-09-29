"""
Plantilla de configuración privada.
1. Copia este archivo como local_settings.py (en esta misma carpeta).
2. Cambia los valores. local_settings.py NO se sube a GitHub (.gitignore).
"""
# Genera una clave con:
# python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
SECRET_KEY = "pega-aqui-tu-clave-secreta"

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# MySQL Community Server 8.4 en local (contraseña de root elegida al instalarlo)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "club_optica",
        "USER": "root",
        "PASSWORD": "tu-contraseña-de-mysql",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}

# En producción (PythonAnywhere) se configurará el SMTP real de la óptica:
# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.tu-proveedor.com"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = ""
# EMAIL_HOST_PASSWORD = ""
