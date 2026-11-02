# Plantilla de local_settings.py, la configuración privada de cada ordenador.
# Copiar como local_settings.py y rellenar los datos. Ese archivo no se sube a Git.

# Para generar una clave:
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY = "pega-aqui-tu-clave-secreta"

# True solo en desarrollo. En producción, False.
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "club_optica_brigantium",
        "USER": "root",
        "PASSWORD": "pega-aqui-tu-contraseña",
        "HOST": "localhost",
        "PORT": "3306",
        "OPTIONS": {"charset": "utf8mb4"},
    }
}