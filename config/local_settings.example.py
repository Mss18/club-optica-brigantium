# Plantilla de local_settings.py, la configuración privada de cada ordenador.
# Copiar como local_settings.py y sustituir SECRET_KEY por una clave real. Ese archivo no se sube a Git.

SECRET_KEY = "pega-aqui-tu-clave-secreta"
DEBUG = False  
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