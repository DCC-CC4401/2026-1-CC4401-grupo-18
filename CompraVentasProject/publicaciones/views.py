from django.shortcuts import render, redirect

from publicaciones.models import Categoria, Publicacion
from publicaciones.forms import PublicacionForm


def publicaciones(request):
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
    return render(request, "publicaciones/buscar.html", {})


def publicar(request):
  if request.method == "POST":
    form_publicacion = PublicacionForm(request.POST, request.FILES)

    if form_publicacion.is_valid():
      form_publicacion.save()
      return redirect("publicaciones")

    return render(request, "publicaciones/publicar.html", {
      "form_publicacion": form_publicacion
    })

  if request.method == "GET":
    form_publicacion = PublicacionForm()
    return render(request, "publicaciones/publicar.html", {
      "form_publicacion": form_publicacion
    })