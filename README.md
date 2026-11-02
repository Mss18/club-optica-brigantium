# Club Óptica Brigantium

Proyecto final del ciclo superior de Desarrollo de Aplicaciones Web (DAW).

Es una web para el club de clientes de una óptica de Betanzos. La óptica publica campañas con beneficios (descuentos, regalos, servicios), los clientes se registran y piden su cupón, y en la tienda un dependiente lo canjea escaneando el código QR.

Esto es la primera entrega. Faltan las métricas para el administrador, los emails y el despliegue.

## Qué se puede hacer ahora

- **Cliente:** crear cuenta, ver las campañas activas, pedir un cupón (con límite por cliente) y consultar sus cupones con el QR.
- **Dependiente:** canjear un cupón escaneando el QR con la cámara, subiendo una imagen o escribiendo el código. Si el cupón no existe, ya se usó o ha caducado, la web lo avisa.
- **Administrador:** crear y editar campañas, beneficios y usuarios desde el panel de administración de Django.

Los tres roles son grupos de Django (Cliente, Dependiente y Administrador). Quien se registra desde la web entra siempre como Cliente; los dependientes los da de alta el administrador.

## Tecnologías

- Python 3.13 y Django 5.2
- MySQL 8
- Bootstrap 5 (por CDN)
- html5-qrcode para el escáner y segno para generar los QR

## Probarlo en local

Hace falta tener instalados Python 3.13, Git y MySQL (en marcha, con un usuario que pueda crear bases de datos).

1. Clonar el repositorio y entrar en la carpeta.
2. Crear el entorno virtual e instalar las dependencias:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copiar `config/local_settings.example.py` como `config/local_settings.py` y rellenarlo con tu clave secreta y los datos de tu MySQL. Este archivo no se sube al repositorio.
4. Instalar:
   ```
   python manage.py instalar
   ```
   Crea la base de datos, las tablas y los tres roles, y te pide usuario, correo y contraseña para la cuenta de administrador.
5. Arrancar el servidor y abrir http://127.0.0.1:8000
   ```
   python manage.py runserver
   ```

El escáner de la cámara solo funciona en `localhost` o con HTTPS.

## Estructura

- `config/`: ajustes y rutas del proyecto
- `cuentas/`: registro, login y usuarios
- `campanas/`: campañas, beneficios, cupones y canjes
- `templates/`: plantilla base
- `docs/`: decisiones técnicas y notas