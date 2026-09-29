# Club Óptica Brigantium

Aplicación web de fidelización y promociones para Óptica Brigantium (Betanzos).
Proyecto final del ciclo de Desarrollo de Aplicaciones Web · IES Fernando Wirtz Suárez · 2026-2027.

**Autor:** Martín Serantes Santos

## Tecnologías
Python 3.12 · Django 5.2 LTS · MySQL 8 · HTML5 · CSS3 · Bootstrap 5 · JavaScript · html5-qrcode · Chart.js · PythonAnywhere

## Instalación en local
```bash
python -m venv .venv
.venv\Scripts\activate            # Windows
pip install -r requirements.txt
copy config\local_settings.example.py config\local_settings.py   # y editarlo
python manage.py instalar         # crea la base de datos, las tablas, los roles y el administrador
python manage.py runserver
```
Abrir http://127.0.0.1:8000

## Estructura
| Carpeta | Contenido |
|---|---|
| `config/` | Configuración del proyecto y URLs principales |
| `cuentas/` | Usuarios, login, registro y roles. Comando `instalar` |
| `club/` | Parte pública y área privada del cliente |
| `campanas/` | Campañas, condiciones y beneficios |
| `cupones/` | Cupones, códigos QR y canjes |
| `panel/` | Panel del personal y métricas |
| `templates/` | Plantillas HTML (base.html y las de cada app) |
| `static/` | CSS, JavaScript e imágenes |
| `docs/` | Documentación y backlog |
