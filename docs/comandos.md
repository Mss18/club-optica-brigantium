# Comandos del proyecto (PowerShell, desde la carpeta del proyecto)

## 0. Antes de nada
.venv\Scripts\activate          # el prompt debe mostrar (.venv)
python manage.py runserver      # arranca la web: http://127.0.0.1:8000/  (parar: Ctrl+C)
# Panel de administración: http://127.0.0.1:8000/admin/

## 1. Instalar desde cero
python manage.py instalar       # crea BD MySQL, migraciones, roles y primer administrador
python manage.py check          # debe decir: no issues

## 2. Cuando cambio un modelo (models.py)
python manage.py makemigrations campanas   # genera el archivo de migración
# -> abrir y leer el archivo nuevo en campanas/migrations/ ANTES de seguir
python manage.py migrate                   # lo aplica a MySQL
python manage.py makemigrations --check    # ¿modelo y BD coinciden? (sin crear nada)
python manage.py showmigrations            # lista migraciones aplicadas [X] y pendientes [ ]

## 3. Probar datos en el shell de Django (escribir cada línea DENTRO del shell)
python manage.py shell          # entra en Python: el prompt cambia a >>>
exit()                          # para salir

# Dentro del shell:
from campanas.models import Campana, Beneficio, Cupon
from cuentas.models import Usuario

Campana.objects.count()                    # cuántas campañas hay
Cupon.objects.all()                        # lista de cupones
Cupon.objects.last().codigo                # código del último cupón (el del QR)
Cupon.objects.filter(estado="activo")      # solo los activos

# Crear un cupón a mano (necesita un cliente y un beneficio que ya existan):
cliente = Usuario.objects.get(username="TU_USUARIO")
beneficio = Beneficio.objects.first()
Cupon.objects.create(cliente=cliente, beneficio=beneficio, fecha_caducidad="2026-12-31")
# El campo codigo se genera solo (UUID). Si falla, revisa que existan cliente y beneficio.

## 4. Git (después de cada paso que funciona)
git status                      # qué ha cambiado
git diff ruta\archivo.py        # ver qué cambió en un archivo (salir con q)
git add ruta\archivo.py         # añadir archivos concretos, nunca "git add ."
git commit -m "Mensaje corto en presente"
git push                        # subir a GitHub
git log --oneline -5            # últimos 5 commits

## 5. Si algo falla
# - "No module named django"      -> falta activar el venv (.venv\Scripts\activate)
# - "from ... no se admite"       -> estás en PowerShell: entra antes al shell de Django
# - Error de MySQL 2002/10061     -> servicio MySQL80 parado (services.msc)
# - Leer el error de ABAJO hacia arriba: la última línea es la causa