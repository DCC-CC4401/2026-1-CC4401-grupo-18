# CompraVentas FCFM

> Plataforma de divulgación de información para apoyar el proceso de compra y venta de productos o servicios dentro de la Facultad de Ciencias Físicas y Matemásticas (FCFM) de la Universidad de Chile.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-green?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/Base%20de%20datos-SQLite-lightgrey?logo=sqlite)
![Status](https://img.shields.io/badge/Estado-En%20desarrollo-orange)

Página web desarrollada con Django mediante la cual la comunidad integrante de la FCFM tiene la posibilidad de publicar y explorar los productos o servicios disponibles para la venta dentro de la facultad. Los usuarios podrán interactuar desde la creación de publicaciones con atributos tales como imagen, descripción y categorías, hasta el uso de filtros o búsqueda de productos disponibles en un momento determinado o la búsqueda de un producto específico.

---
## ✨ Funcionalidades:

- 📋 **Listado de publicaciones** — se visualizan todos los productos disponibles ordenados por fecha de publicación desde la más reciente hasta la más antigua.
- 🏷️ **Filtrado por categoría** — se filtran las publicaciones según su categoría.
- 🔍 **Búsqueda de productos** — se encuentran productos o servicios específicos.
- 📝 **Publicar productos** — formulario para subir título, descripción, imagen y categorías de los productos.
- 🗂️ **Panel de administración** — gestión completa de publicaciones y categorías desde `/admin`
---

## 🛠️ Tecnologías

| Tecnología | Uso |
|---|---|
| Python 3.10+ | Lenguaje principal |
| Django 6.0 | Framework web |
| SQLite | Base de datos (desarrollo) |
| Pillow | Procesamiento de imágenes |

---

## 🚀 Instalación y ejecución local

### Prerrequisitos

- Python 3.10 o superior
- pip
- Git

### Pasos a seguir

**1. Clonar el repositorio**

```bash
git clone https://github.com/DCC-CC4401/2026-1-CC4401-grupo-18.git
cd 2026-1-CC4401-grupo-18
```

**2. Crear y activar un entorno virtual**
```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Aplicar migraciones**
```bash
python manage.py makemigrations
python manage.py migrate
```

**5. (Opcional) Crear un superusuario propio**
```bash
python manage.py createsuperuser
```

**6. Levantar el servidor de desarrollo**
```bash
python manage.py runserver
```

Visita: [http://127.0.0.1:8000/publicaciones](http://127.0.0.1:8000/publicaciones)

---

## 🗺️ URLs disponibles

| URL | Descripción |
|---|---|
| `/publicaciones/` | Página principal con listado de publicaciones de productos o servicios y filtro por categoría |
| `/publicar/` | Formulario para crear una nueva publicación |
| `/buscar/` | Buscador de productos o servicios |
| `/admin/` | Panel de administración de Django |

---

## 🗃️ Estructura del proyecto

```text
2026-1-CC4401-GRUPO-18/
│
├── CompraVentasProject/
│   │
│   ├── CompraVentasProject/              # Configuración principal del proyecto Django
│   │   ├── __init__.py
│   │   ├── settings.py                    # Configuración global
│   │   ├── urls.py                        # URLs principales
│   │   ├── asgi.py                        # Configuración ASGI
│   │   └── wsgi.py                        # Configuración WSGI
│   │
│   ├── publicaciones/                     # Aplicación principal
│   │   ├── imagenes/                      # Imágenes de publicaciones
│   │   ├── migrations/                    # Migraciones de base de datos
│   │   │   └── 0001_initial.py
│   │   │
│   │   ├── static/                        # Archivos estáticos CSS/JS
│   │   │   └── styles.css
│   │   │
│   │   ├── templates/
│   │   │   └── publicaciones/             # Templates HTML
│   │   │       ├── buscar.html
│   │   │       ├── pagina_principal.html
│   │   │       └── publicar.html
│   │   │
│   │   ├── admin.py                       # Configuración panel de administración
│   │   ├── apps.py                        # Configuración interna de la app
│   │   ├── forms.py                       # Formulario de publicaciones
│   │   ├── models.py                      # Modelos de datos
│   │   ├── tests.py                       # Pruebas unitarias y validación del sistema
│   │   ├── urls.py                        # URLs de la aplicación
│   │   └── views.py                       # Lógica de las vistas: publicaciones, buscar, publicar
│   │
│   ├── db.sqlite3                         # Base de datos SQLite
│   └── manage.py                          # Administrador del proyecto Django
│
├── .gitignore                             # Archivos ignorados por Git
├── README.md                              # Documentación del proyecto
└── requirements.txt                       # Dependencias del proyecto
```

---
## 🧩 Modelos

### `Categoria`
| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | CharField (64) | Nombre de la categoría |

### `Publicacion`
| Campo | Tipo | Descripción |
|---|---|---|
| `titulo` | CharField (128) | Título único del producto |
| `descripcion` | TextField | Descripción del producto |
| `imagen` | ImageField | Foto del producto |
| `fecha_creacion` | DateField | Fecha de publicación |
| `categorias` | ManyToManyField | Categorías asociadas |

---

## 🔑 Acceso al panel de administración

El panel de administración en `/admin` que tiene integrada Django es posible crear y gestionar publicaciones y categorías de forma visual.
Con esta cuenta se pueden crear publicaciones y categorias de manera
intuitiva con la GUI de `/admin` que trae integrada Django.

Existen **2 publicaciones** y **5 categorías** de ejemplo para explorar la visualización de los `.html`..

> ⚠️ **La cuenta de prueba es solo para desarrollo local. Eliminarla antes de cualquier despliegue en producción.**

```
URL:      http://127.0.0.1:8000/admin
Usuario:  test
Email:    test@test.dev
Password: 12345678
```

---

## 👥 Integrantes

| Nombre | GitHub |
|---|---|
| Felipe Arriagada | [xXTheNyanLord777Xx](https://github.com/xXTheNyanLord777Xx) |
| Héctor Bonilla | [esnore-hb](https://github.com/esnore-hb) |
| Matías Ávalos | [maty-aval00s](https://github.com/maty-aval00s) |
| Sofía Silva | [sofisilvva](https://github.com/sofisilvva) |
| Yuly Ramírez | [YULYRAMIREZ](https://github.com/YULYRAMIREZ) |

---

## 📝 Contexto académico

Este proyecto es desarrollado en el marco de las actividades del curso **CC4401 — Ingeniería de Software** del Departamento de Ciencias de la Computación, Universidad de Chile.

[![CC BY-NC 4.0](https://img.shields.io/badge/Licencia-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)



