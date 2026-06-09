from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url='/publicaciones/', permanent=False)),
    path("publicaciones/", views.publicaciones, name="publicaciones"),
    path("buscar/", views.buscar, name="buscar"),
    path("publicar/", views.publicar, name="publicar"),
]
