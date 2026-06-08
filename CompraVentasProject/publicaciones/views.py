"""Vistas de la aplicación de publicaciones.

Contiene las vistas que manejan las páginas principales de la plataforma:
- `publicaciones`: página principal con listado de publicaciones y filtro por categoría.
- `buscar`: página de búsqueda de productos o servicios.
- `publicar`: formulario para crear una nueva publicación.

Cada vista solo responde a los métodos HTTP que tiene definidos, tales como:
- GET: `publicaciones`, `buscar`, `publicar`
- POST:`publicar`

Si llega cualquier otro método, la vista lo ignora y retorna None.
"""
from django.db.models import Q
from django.shortcuts import redirect, render

from publicaciones.forms import PublicacionForm
from publicaciones.models import Categoria, Publicacion


def publicaciones(request):
    """Muestra la página principal con todas las publicaciones disponibles.

    Obtiene todas las publicaciones ordenadas por fecha de creación (más reciente primero)
    y las categorías existentes para el menú de filtros.

    Si se recibe el parámetro GET 'categoria', filtra las publicaciones para mostrar solo
    las que pertenecen a esa categoría.

    Args:
       request: Objeto HttpRequest de Django.

    Returns:
        HttpResponse con el template 'publicaciones/pagina_principal.html',
        incluyendo las publicaciones, categorias y la categoría activa.
        Retorna None si el método HTTP no es GET.

    Context:
        publicaciones: QuerySet (resultado de una consulta a la base de datos) de Publicaciones 
                       ordenadas de la más reciente a la más antigua. En caso de la misma fecha,
                       se desempata por id en orden descedente.
        categorias: QuerySet con todas las categorías disponibles.
        c_activa: ID de la categoría seleccionada por el usuario para filtrar las publicaciones.
                  Si el usuario no seleccionó ninguna categoría, viene vacío ('').
    """
    # Obtener todas las publicaciones, las más recientes primero
    publicaciones = Publicacion.objects.all().order_by("-fecha_creacion", "-id")
    categorias = Categoria.objects.all()

    # Leer el filtro de categoría desde los parámetros GET (?categoria=<id>)
    # Ejemplo de URL: /publicaciones/?categoria=3
    c_id = request.GET.get("categoria", "")

    # Si se especificó una categoría, filtrar las publicaciones
    if c_id:
        publicaciones = publicaciones.filter(categorias__id=c_id)

    if request.method == "GET":
        return render(
            request,
            "publicaciones/pagina_principal.html",
            {
                "publicaciones": publicaciones,
                "categorias": categorias,
                "c_activa": c_id,# Le pasa al template el ID de la categoría seleccionada para resaltarla visualmente
            },
        )
    return None




def buscar(request):
    """Muestra la página de búsqueda de productos o servicios.

    Actualmente solo renderiza la página de búsqueda.
    La lógica de búsqueda aún no está implementada.

    Args:
        request: Objeto HttpRequest de Django que contiene información de la solicitud
         del usuario, como el método HTTP (GET).

    Returns:
        HttpResponse con el template 'publicaciones/buscar.html'.
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

    - En GET: muestra el formulario vacío para ingresar los datos del producto.
    - En POST: valida y guarda la nueva publicación. Si el formulario es válido,
      redirige a la página principal. Si no, vuelve a mostrar el formulario con 
      los errores de validación.

    Args:
        request: Objeto HttpRequest de Django que contiene información de la solicitud
         del usuario, como el método HTTP (GET o POST), los parámetros de la
         URL y los datos del formulario (título, descripción, imagen y categorías)
         en caso de ser POST.

    Returns:
        GET: HttpResponse con el template 'publicaciones/publicar.html'
             y un formulario vacío para que el usuario diligencie la información.
        POST válido: Redirige a la vista 'publicaciones' tras guardar.
        POST inválido: HttpResponse con el template y el formulario con errores 
                       (por ejemplo, dejó un campo vacío).
        Retorna None si el método HTTP no es GET ni POST.

    """
    if request.method == "POST":
        # Inicializar el formulario con los datos enviados, incluyendo archivos (imagen)
        form_publicacion = PublicacionForm(request.POST, request.FILES)

        if form_publicacion.is_valid():
            # Guardar la publicación en la base de datos y redirigir al listado
            form_publicacion.save()
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
