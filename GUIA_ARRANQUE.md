# Guía de arranque del proyecto

Pasos para dejar todo preparado y empezar a desarrollar el Club Óptica Brigantium en Windows.
Sigue el orden: cada paso depende del anterior.

---

## 1. Instalar las herramientas

| Herramienta | Dónde | Notas |
|---|---|---|
| Python 3.12 | https://www.python.org/downloads/ | Versión 3.12 de 64 bits. En el instalador marca **"Add python.exe to PATH"**. |
| MySQL Community Server 8.4 y MySQL Workbench | https://dev.mysql.com/downloads/installer/ | Elige la instalación con servidor y Workbench. Apunta la contraseña de `root`. |
| Git | https://git-scm.com/download/win | Opciones por defecto. |
| Visual Studio Code | https://code.visualstudio.com/ | Extensiones: **Python** (Microsoft) y **Django** (Baptiste Darthenay). |
| GitHub CLI (opcional) | https://cli.github.com/ | Solo para crear las tareas en GitHub con el script. |

> **Importante: no uses el MySQL de XAMPP.** XAMPP trae MariaDB 10.4, y Django 5.2 necesita MariaDB 10.5 o superior (o MySQL 8). Con XAMPP la aplicación no arrancará. En la memoria, cambia la fila "XAMPP (MySQL)" de la tabla de software por "MySQL Community Server 8.4".

Comprueba en una terminal (PowerShell) que todo está instalado:
```powershell
python --version      # Python 3.12.x
git --version
```

---

## 2. Crear el repositorio en GitHub

1. En GitHub, crea un repositorio llamado `club-optica-brigantium`, **sin** README (ya viene en el paquete).
2. Si lo haces privado, añade a los tutores como colaboradores más adelante (o hazlo público antes de la entrega).
3. Descomprime el paquete en tu carpeta de trabajo y, desde PowerShell dentro de la carpeta:

```powershell
git init
git add .
git commit -m "Estructura inicial del proyecto"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/club-optica-brigantium.git
git push -u origin main
```

---

## 3. Preparar el entorno de Python

Dentro de la carpeta del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Verás `(.venv)` al principio de la línea: eso indica que el entorno virtual está activo. Tendrás que activarlo cada vez que abras una terminal nueva (VS Code lo hace solo si seleccionas el intérprete de `.venv`).

> Si PowerShell no deja ejecutar `activate`, ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## 4. Configuración privada

1. Copia la plantilla:
   ```powershell
   copy config\local_settings.example.py config\local_settings.py
   ```
2. Genera una clave secreta y pégala en `SECRET_KEY`:
   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
   ```
3. Pon la contraseña de `root` de MySQL en `PASSWORD`.

`local_settings.py` está en `.gitignore`: nunca se sube a GitHub.

---

## 5. Instalar la base de datos y arrancar

Con MySQL en marcha (se inicia solo como servicio de Windows):

```powershell
python manage.py instalar
python manage.py runserver
```

`instalar` es el comando de autoinstalación del proyecto (requisito del módulo): crea la base de datos, las tablas, los roles y te pide los datos del primer administrador.

Abre http://127.0.0.1:8000 y deberías ver la página de inicio del club. Prueba también a iniciar sesión con el administrador.

---

## 6. Qué hay en el paquete

| Carpeta o archivo | Para qué sirve |
|---|---|
| `config/settings.py` | Configuración: apps, idioma, zona horaria, ficheros estáticos, correo. |
| `config/local_settings.example.py` | Plantilla de la configuración privada. |
| `cuentas/models.py` | Modelo `Usuario` (hereda de `AbstractUser`) y nombres de los roles. |
| `cuentas/management/commands/instalar.py` | Comando de autoinstalación. |
| `club/`, `campanas/`, `cupones/`, `panel/` | Apps de cada módulo. Los modelos de campañas y cupones están comentados, a la espera del diseño de la BD. |
| `templates/base.html` | Plantilla base con Bootstrap, Poppins y la cabecera. Todas las páginas heredan de ella. |
| `static/css/estilos.css` | Colores y estilos de la guía de estilo como variables CSS. |
| `static/js/app.js` | Validación de formularios en el navegador. |
| `docs/backlog.md` | Todas las tareas del proyecto por bloques. |
| `scripts/crear_issues.ps1` | Crea esas tareas como issues en GitHub. |

**Por qué el modelo de usuario ya está creado:** Django recomienda definir el modelo de usuario propio antes de la primera migración; cambiarlo después es muy complicado. Por eso es lo único que va adelantado.

---

## 7. Organizar las tareas en GitHub

1. En tu repositorio, pestaña **Projects** → **New project** → plantilla **Board** (columnas: Todo, In Progress, Done).
2. Crea las tareas del backlog:
   - Con GitHub CLI: `gh auth login` y después `.\scripts\crear_issues.ps1`.
   - O a mano, copiando los títulos de `docs/backlog.md`.
3. Añade las issues al tablero y ve moviéndolas según avances.

Para enlazar cada commit con su tarea, incluye el número de la issue en el mensaje, por ejemplo `git commit -m "Registro de clientes #12"`. En la defensa, el tablero y el historial de commits demuestran el seguimiento del proyecto.

---

## 8. Crear el Proyecto en Claude

Sube como conocimiento:
- La memoria entregada y la guía de estilo.
- Los requisitos de DWCS y las indicaciones generales del módulo (del aula virtual).
- La plantilla de la memoria.
- Más adelante: el modelo de la base de datos y los wireframes.

Instrucciones del Proyecto (ajústalas a tu gusto):

> Estoy desarrollando el proyecto final del ciclo DAW: una aplicación web de club de clientes para una óptica, siguiendo la memoria y la guía de estilo adjuntas. Stack: Python 3.12, Django 5.2 LTS, MySQL 8, HTML, CSS, Bootstrap 5, JavaScript, html5-qrcode y Chart.js, con publicación en PythonAnywhere. Soy nuevo en Python y Django: explícame el código que propongas y por qué, porque tengo que defenderlo ante un tribunal. Prioriza soluciones sencillas que cumplan los requisitos del módulo. No amplíes el alcance sin avisarme. Responde en español.

Usa una conversación por tarea o por bloque ("Modelo de la base de datos", "Bloque 1: registro y login"…).

---

## 9. Primeras tareas (hasta el 16 de octubre)

1. **Modelo de la base de datos.** Es lo más importante del diseño, porque de él dependen el resto de tareas. Entidades principales: usuario, campaña, beneficio (con sus tipos), condición, cupón y canje. Dibújalo en MySQL Workbench.
2. **Casos de uso** de los tres roles.
3. **Wireframes** en Figma de las pantallas principales, en móvil y escritorio.
4. **Publicación de prueba en PythonAnywhere.** Sube esta versión inicial cuanto antes: los problemas de publicación se resuelven mejor al principio que la semana de la entrega. Comprueba qué incluye cada plan (base de datos MySQL, tareas programadas, dominio propio).

---

## 10. Aprender Django

- Tutorial oficial en español: https://docs.djangoproject.com/es/5.2/intro/tutorial01/ (las partes 1 a 4 cubren modelos, vistas, plantillas y formularios).
- Tutorial de Django Girls en español: https://tutorial.djangogirls.org/es/ (muy guiado, ideal para empezar).

Te recomiendo hacer las cuatro primeras partes del tutorial oficial antes del Bloque 1: son unas pocas horas y ahorran mucho tiempo después.

---

## 11. Problemas frecuentes

| Problema | Solución |
|---|---|
| `Falta config/local_settings.py` | No has copiado la plantilla (paso 4). |
| Error al instalar `mysqlclient` | Comprueba que usas Python 3.12 de 64 bits y actualiza pip: `python -m pip install --upgrade pip`. |
| `Access denied for user 'root'` | La contraseña de `local_settings.py` no coincide con la de MySQL. |
| `Can't connect to MySQL server` | MySQL no está en marcha: búscalo en Servicios de Windows (MySQL84) e inícialo. |
| `MariaDB 10.5 or later is required` | Estás usando el MySQL de XAMPP. Usa MySQL Community Server (paso 1). |
