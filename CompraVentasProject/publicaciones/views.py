from django.shortcuts import render, redirect

from publicaciones.models import Categoria, Publicacion

def publicaciones(request):
  publicaciones = Publicacion.objects.all()
  categorias = Categoria.objects.all()
  c_id = request.GET.get('categoria', '')

  if c_id:
    publicaciones = publicaciones.filter(categorias__id=c_id)
  
  if request.method == "GET":
    return render(request, "publicaciones/pagina_principal.html", {
      'publicaciones':publicaciones,
      'categorias':categorias,
      'c_activa':c_id
    })


def buscar(request):
  

  if request.method == "GET":
    return render(request, "publicaciones/buscar.html", {})

def publicar(request):
  

  if request.method == "GET":
    return render(request, "publicaciones/publicar.html", {})
  

