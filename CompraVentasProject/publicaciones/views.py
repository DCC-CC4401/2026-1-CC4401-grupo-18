"""Vistas de la aplicación de publicaciones.

Contiene las vistas que manejan las páginas principales de la plataforma:

- `publicaciones`: página principal con listado de publicaciones y filtro por categoría.
- `buscar`: página de búsqueda de productos o servicios.
- `publicar`: formulario para crear una nueva publicación (requiere autenticación).
- `registro`: formulario de registro de nuevos usuarios.
- `iniciar_sesion`: formulario de inicio de sesión.
- `cerrar_sesion`: cierre de sesión del usuario autenticado.

Cada vista solo responde a los métodos HTTP que tiene definidos, tales como:
- GET: `publicaciones`, `buscar`, `publicar`, `registro`, `iniciar_sesion`
- POST: `publicar`, `registro`, `iniciar_sesion`, `cerrar_sesion`

Si llega cualquier otro método, la vista lo ignora y retorna None.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from django.shortcuts import redirect, render

from publicaciones.forms import LoginForm, PublicacionForm, RegistroForm
from publicaciones.models import Categoria, Publicacion


def publicaciones(request):
    """Muestra la página principal con todas las publicaciones disponibles.

    Obtiene todas las publicaciones ordenadas por fecha de creación (más reciente primero)
    y las categorías existentes para el menú de filtros.

    Si se recibe el parámetro GET ``categoria``, filtra las publicaciones para mostrar solo
    las que pertenecen a esa categoría.

    Si se recibe el parámetro GET ``q``, filtra las publicaciones cuyo título, descripción
    o categoría contengan el texto buscado.

    Args:
        request: Objeto HttpRequest de Django que contiene información de la solicitud
            del usuario, como el método HTTP (GET) y los parámetros ``categoria`` y ``q``.

    Returns:
        HttpResponse con el template ``publicaciones/pagina_principal.html``,
        incluyendo las publicaciones, categorías, categoría activa y texto buscado.
        Retorna None si el método HTTP no es GET.
    """
    # Obtener todas las publicaciones, las más recientes primero
    publicaciones = Publicacion.objects.all().order_by("-fecha_creacion", "-id")
    categorias = Categoria.objects.all()

    # Leer los filtros desde los parámetros GET
    # Ejemplo de URL: /publicaciones/?categoria=3&q=texto
    c_id = request.GET.get("categoria", "").strip()
    q = request.GET.get("q", "").strip()

    # Si se especificó una categoría, filtrar las publicaciones por ella
    if c_id:
        publicaciones = publicaciones.filter(categorias__id=c_id)
    
    # Si se especificó un texto, filtrar por título, descripción o nombre de categoría
    if q:
        publicaciones = publicaciones.filter(
            Q(titulo__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(categorias__nombre__icontains=q)
        )

    publicaciones = publicaciones.distinct().order_by("-fecha_creacion", "-id")

    if request.method == "GET":
        return render(
            request,
            "publicaciones/pagina_principal.html",
            {
                "publicaciones": publicaciones,
                "categorias": categorias,
                "c_activa": c_id, # El ID de la categoría seleccionada se pasa al template para resaltarla visualmente
                "q": q,
            },
        )
    return None


def buscar(request):
    """Muestra resultados de búsqueda de productos o servicios.

    Filtra las publicaciones según los parámetros GET ``categoria`` y ``q``,
    y renderiza los resultados en la página principal.

    Args:
        request: Objeto HttpRequest de Django que contiene información de la solicitud
            del usuario, como el método HTTP (GET) y los parámetros ``categoria`` y ``q``.

    Returns:
        HttpResponse con el template ``publicaciones/pagina_principal.html``,
        incluyendo las publicaciones filtradas, categorías, categoría activa y texto buscado.
        Retorna None si el método HTTP no es GET.

    """
    if request.method == "GET":
        publicaciones = Publicacion.objects.all()
        categorias = Categoria.objects.all()

        c_id = request.GET.get("categoria", "").strip()
        q = request.GET.get("q", "").strip()

        if c_id:
            publicaciones = publicaciones.filter(categorias__id=c_id)

        if q:
            publicaciones = publicaciones.filter(
                Q(titulo__icontains=q)
                | Q(descripcion__icontains=q)
                | Q(categorias__nombre__icontains=q)
            )

        publicaciones = publicaciones.distinct().order_by(
            "-fecha_creacion", "-id"
        )

        return render(
            request,
            "publicaciones/pagina_principal.html",
            {
                "publicaciones": publicaciones,
                "categorias": categorias,
                "c_activa": c_id,
                "q": q,
            },
        )
    return None


def publicar(request):
    """Permite crear una nueva publicación en la plataforma.

    Requiere que el usuario esté autenticado. Si no lo está, redirige
    a la página de inicio de sesión.

    - En GET: muestra el formulario vacío para ingresar los datos del producto.
    - En POST con datos válidos: guarda la nueva publicación y redirige a la página principal. 
    - En POST con datos inválidos: vuelve a mostrar el formulario con los errores.

    Si se ingresó una nueva categoría en el formulario, se crea o reutiliza la categoría
    existente y se asocia a la publicación.

    Args:
        request: Objeto HttpRequest de Django que contiene información de la solicitud
            del usuario, como el método HTTP (GET o POST), los parámetros de la URL y los datos 
            del formulario (título, descripción, imagen, categorías, precio, disponibilidad, 
            nombre del vendedor, ubicación, correo electrónico y teléfono) en caso de ser POST.

    Returns:
        GET: HttpResponse con el template ``publicaciones/publicar.html``
             y un formulario vacío mediante el cual el usuario diligencia la información.
        POST válido: Redirige a la vista ``publicaciones`` tras guardar.
        POST inválido: HttpResponse con el template y el formulario con errores 
                      (por ejemplo, hay algún campo vacío).
        Retorna None si el método HTTP no es GET ni POST.

    """
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        # Inicializar el formulario con los datos enviados, incluyendo archivos (imagen)
        form_publicacion = PublicacionForm(request.POST, request.FILES)

        if form_publicacion.is_valid():
            # Guardar la publicación sin confirmar aún para poder adicionar relaciones Many-to-many (m2m)
            publicacion = form_publicacion.save(commit = False)
            publicacion.save()
            form_publicacion.save_m2m()

            # Si el usuario ingresó una nueva categoría, crearla o reutilizar una existente.
            nueva_categoria = (form_publicacion.cleaned_data["nueva_categoria"].strip().title())
            if nueva_categoria:
                categoria, _ = Categoria.objects.get_or_create(nombre=nueva_categoria)
                publicacion.categorias.add(categoria)

            return redirect("/publicaciones/#publicaciones")

        # Si el formulario tiene errores, volver a renderizarlo con los mensajes de error
        return render(
            request,
            "publicaciones/publicar.html",
            {"form_publicacion": form_publicacion},
        )

    if request.method == "GET":
        # Mostrar el formulario vacío para que el usuario ingrese los datos
        form_publicacion = PublicacionForm()
        return render(
            request,
            "publicaciones/publicar.html",
            {"form_publicacion": form_publicacion},
        )
    return None


def registro(request):
    """Muestra y procesa el formulario de registro de nuevos usuarios.

    - En GET: muestra el formulario de registro vacío.
    - En POST: valida los datos ingresados. Si son válidos, crea el usuario,
      inicia sesión automáticamente y redirige a la página principal.
      Si no son válidos, vuelve a mostrar el formulario con los errores.

    Args:
        request: Objeto HttpRequest de Django.

    Returns:
        GET: HttpResponse con el template 'publicaciones/registro.html'.
        POST válido: Redirige a la vista 'publicaciones'.
        POST inválido: HttpResponse con el formulario y errores de validación.
    """
    if request.user.is_authenticated:
        return redirect("publicaciones")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Cuenta creada exitosamente! Bienvenido/a.")
            return redirect("publicaciones")
        return render(
            request,
            "publicaciones/registro.html",
            {"form": form},
        )

    if request.method == "GET":
        form = RegistroForm()
        return render(
            request,
            "publicaciones/registro.html",
            {"form": form},
        )
    return None


def iniciar_sesion(request):
    """Muestra y procesa el formulario de inicio de sesión.

    - En GET: muestra el formulario de login vacío.
    - En POST: valida las credenciales. Si son correctas, inicia sesión
      y redirige a la página principal. Si no, muestra un error.

    Args:
        request: Objeto HttpRequest de Django.

    Returns:
        GET: HttpResponse con el template 'publicaciones/login.html'.
        POST válido: Redirige a la vista 'publicaciones'.
        POST inválido: HttpResponse con el formulario y errores.
    """
    if request.user.is_authenticated:
        return redirect("publicaciones")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Django usa username para autenticar; en nuestro caso username = email
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("publicaciones")
            else:
                form.add_error(None, "Correo o contraseña incorrectos.")
        return render(
            request,
            "publicaciones/login.html",
            {"form": form},
        )

    if request.method == "GET":
        form = LoginForm()
        return render(
            request,
            "publicaciones/login.html",
            {"form": form},
        )
    return None


def cerrar_sesion(request):
    """Cierra la sesión del usuario autenticado y redirige a la página principal.

    Args:
        request: Objeto HttpRequest de Django.

    Returns:
        Redirige a la vista 'publicaciones'.
    """
    logout(request)
    return redirect("publicaciones")

