<<<<<<< Updated upstream
from django.shortcuts import render, redirect
=======
from django.db.models import Q
from django.shortcuts import redirect, render
>>>>>>> Stashed changes

from publicaciones.models import Categoria, Publicacion
from publicaciones.forms import PublicacionForm


def publicaciones(request):
<<<<<<< Updated upstream
  publicaciones = Publicacion.objects.all().order_by("-fecha_creacion", "-id")
  categorias = Categoria.objects.all()
  c_id = request.GET.get('categoria', '')

  if c_id:
    publicaciones = publicaciones.filter(categorias__id=c_id)
  
  if request.method == "GET":
    return render(request, "publicaciones/pagina_principal.html", {
      'publicaciones': publicaciones,
      'categorias': categorias,
      'c_activa': c_id
    })


def buscar(request):
  if request.method == "GET":
=======
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

    publicaciones = publicaciones.distinct().order_by("-fecha_creacion", "-id")

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


def buscar(request):
>>>>>>> Stashed changes
    return render(request, "publicaciones/buscar.html", {})


def publicar(request):
  if request.method == "POST":
    form_publicacion = PublicacionForm(request.POST, request.FILES)

<<<<<<< Updated upstream
    if form_publicacion.is_valid():
      form_publicacion.save()
      return redirect("publicaciones")
=======
        if form_publicacion.is_valid():
            form_publicacion.save()
            return redirect("/publicaciones/#publicaciones")
>>>>>>> Stashed changes

    return render(request, "publicaciones/publicar.html", {
      "form_publicacion": form_publicacion
    })

<<<<<<< Updated upstream
  if request.method == "GET":
    form_publicacion = PublicacionForm()
    return render(request, "publicaciones/publicar.html", {
      "form_publicacion": form_publicacion
    })
=======
    form_publicacion = PublicacionForm()
    return render(
        request,
        "publicaciones/publicar.html",
        {"form_publicacion": form_publicacion},
    )
>>>>>>> Stashed changes
