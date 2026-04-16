"""Modelo de Publicaciones con sus categorias.

Se proveen las clases `Categoria` y `Publicacion`.
Publicacion tiene una
"""

from django.db import models
from django.utils import timezone


class Categoria(models):
    nombre = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.nombre


class Publicacion(models):
    titulo = models.CharField(max_length=64, blank=False)
    descripcion = models.TextField(blank=False)
    fecha_creacion = models.DateField(
        default=timezone.now().strftime("%Y-%m-%d"),
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
    )

    # TODO: revisar si incluir aqui la imagen, o el ID de la
    # imagen para que la encuentre desde otra ubicacion
