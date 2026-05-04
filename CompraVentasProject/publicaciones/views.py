from django.shortcuts import render, redirect

from publicaciones.models import Categoria, Publicacion

def publicaciones(request):
  publicaciones = Publicacion.objects.all()

  
  if request.method == "GET":
    return render(request, "publicaciones/pagina_principal.html", {})


def buscar(request):
  

  if request.method == "GET":
    return render(request, "publicaciones/buscar.html", {})

def publicar(request):
  

  if request.method == "GET":
    return render(request, "publicaciones/publicar.html", {})
  

