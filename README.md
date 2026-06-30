# CompraVentas FCFM

> Plataforma de divulgación de información para apoyar el proceso de compra y venta de productos o servicios dentro de la Facultad de Ciencias Físicas y Matemásticas (FCFM) de la Universidad de Chile.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-green?logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/Base%20de%20datos-SQLite-lightgrey?logo=sqlite)

Página web desarrollada con Django mediante la cual la comunidad integrante de la FCFM tiene la posibilidad de publicar y explorar los productos o servicios disponibles para la venta dentro de la facultad. Los usuarios podrán interactuar desde la creación de publicaciones con atributos tales como imagen, descripción y categorías, hasta el uso de filtros o búsqueda de productos disponibles en un momento determinado o la búsqueda de un producto específico.

---

## ✨ Funcionalidades

- 📋 **Listado de publicaciones** — se visualizan todos los productos disponibles ordenados por fecha de publicación desde la más reciente hasta la más antigua.
- 🏷️ **Filtrado por categoría** — se filtran las publicaciones según su categoría.
- 🔍 **Búsqueda de productos** — se encuentran productos o servicios específicos.
- 🔎 **Detalle de la publicación** ("ver más") — ventana con la información completa del producto o servicio y los datos de contacto del vendedor.
- 📝 **Publicar productos** — formulario para subir título, descripción, imagen y categorías de los productos.
- ✏️ **Edición de publicaciones** — cada vendedor autenticado puede editar únicamente sus propias publicaciones.
- 🔐 **Registro e inicio de sesión** — creación de cuenta y autenticación de vendedores.
- 👤 **Perfil de vendedor** — página que reúne los datos del usuario y sus publicaciones.
- 🗂️ **Panel de administración** — gestión completa de publicaciones y categorías desde `/admin`

---

## 🛠️ Tecnologías

| Tecnología | Uso |
| --- | --- |
| Python 3.10+ | Lenguaje principal |
| Django 6.0 | Framework web |
| SQLite | Base de datos (desarrollado) |
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
| `/publicaciones/` | Página principal con listado de publicaciones, búsqueda y filtro por categoría |
| `/buscar/` | Buscador de productos o servicios |
| `/publicar/` | Formulario para crear una nueva publicación (requiere inicio de sesión) |
| `/editar/<id>/` | Edición de una publicación propia (requiere inicio de sesión) |
| `/registro/` | Formulario de registro de nuevos usuarios |
| `/login/` | Inicio de sesión |
| `/logout/` | Cierre de sesión |
| `/perfil/` | Perfil propio del usuario autenticado |
| `/perfil/<id>/` | Perfil público de un vendedor |
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
│   │   │
│   │   ├── static/                        # Archivos estáticos CSS/JS
│   │   │   └── styles.css
│   │   │
│   │   ├── templates/
│   │   │   └── publicaciones/             # Templates HTML
│   │   │       ├── pagina_principal.html  # Listado, búsqueda, filtros, detalle y edición
│   │   │       ├── buscar.html
│   │   │       ├── publicar.html          # Formulario de creación de publicaciones
│   │   │       ├── registro.html          # Formulario de registro
│   │   │       ├── login.html             # Formulario de inicio de sesión
│   │   │       └── perfil.html            # Perfil de usuario y sus publicaciones
│   │   │
│   │   ├── admin.py                       # Configuración panel de administración
│   │   ├── apps.py                        # Configuración interna de la app
│   │   ├── forms.py                       # Formularios: registro, inicio de sesión y publicación
│   │   ├── models.py                      # Modelos de datos
│   │   ├── tests.py                       # Pruebas del sistema
│   │   ├── urls.py                        # URLs de la aplicación
│   │   └── views.py                       # Lógica de las vistas
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
| --- | --- | --- |
| `nombre` | CharField (64) | Nombre de la categoría |

### `Publicacion`

| Campo | Tipo | Descripción |
| --- | --- | --- |
| `titulo` | CharField (128) | Título del producto o servicio (mínimo 3 caracteres) |
| `descripcion` | TextField | Descripción del producto o servicio |
| `imagen` | ImageField | Foto del producto o servicio |
| `precio` | PositiveIntegerField | Precio en pesos chilenos |
| `ubicacion` | CharField (128) | Lugar del producto o donde se presta el servicio |
| `disponibilidad` | CharField (choices) | Estado: `DISPONIBLE`, `RESERVADO` o `NO_DISPONIBLE` |
| `nombre_vendedor` | CharField (128) | Nombre del vendedor (se completa desde la cuenta) |
| `correo_electronico` | EmailField | Correo de contacto (se completa desde la cuenta) |
| `telefono` | CharField (12) | Teléfono de contacto del vendedor |
| `fecha_creacion` | DateField | Fecha de publicación |
| `usuario` | ForeignKey (User) | Vendedor que creó la publicación |
| `categorias` | ManyToManyField | Categorías asociadas |

---

## 🔑 Acceso al panel de administración

El panel de administración en `/admin` que tiene integrada Django es posible crear y gestionar publicaciones y categorías de forma visual.
Con esta cuenta se pueden crear publicaciones y categorias de manera
intuitiva con la GUI de `/admin` que trae integrada Django.

Existen **2 publicaciones** y **5 categorías** de ejemplo para explorar la visualización de los `.html`..

> ⚠️ **La cuenta de prueba es solo para desarrollo local. Eliminarla antes de cualquier despliegue en producción.**

```swift
URL:      "http://127.0.0.1:8000/admin"
Usuario:  test
Email:    test@test.dev
Password: 12345678
```

---

## 👥 Integrantes

| Nombre | GitHub |
| --- | --- |
| Felipe Arriagada | [xXTheNyanLord777Xx](https://github.com/xXTheNyanLord777Xx) |
| Héctor Bonilla | [esnore-hb](https://github.com/esnore-hb) |
| Matías Ávalos | [maty-aval00s](https://github.com/maty-aval00s) |
| Sofía Silva | [sofisilvva](https://github.com/sofisilvva) |
| Yuly Ramírez | [YULYRAMIREZ](https://github.com/YULYRAMIREZ) |

---
