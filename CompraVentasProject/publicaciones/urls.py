from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path("", RedirectView.as_view(url='/publicaciones/', permanent=False)),
    path("publicaciones/", views.publicaciones, name="publicaciones"),
    path("buscar/", views.buscar, name="buscar"),
    path("publicar/", views.publicar, name="publicar"),
    path("editar/<int:pk>/", views.editar_publicacion, name="editar_publicacion"),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("perfil/", views.mi_perfil, name="mi_perfil"),
    path("perfil/<int:user_id>/", views.perfil, name="perfil"),
]

