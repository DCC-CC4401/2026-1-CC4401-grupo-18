"""Modelo de Publicaciones con sus categorias.

Se proveen las clases `Categoria` y `Publicacion`.
Publicacion tiene una relacioin con Categoria, donde cada publicacion puede
tener estrictamente mas de una categoria, y cada categoria puede estar en mas
de una publicacion o no estar.

No olvidar ejecutar:
$ python manage.py makemigrations
$ python manage.py migrate

Ante cualquier cambio a los modelos, y luego tener que hacer los cambios
respectivos a los elementos que ya estaban en estos modelos.
"""

from django.db import models
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.nombre


class Publicacion(models.Model):
    titulo = models.CharField(max_length=128, blank=False, unique=True)
    descripcion = models.TextField(blank=False)

    imagen = models.ImageField(
        upload_to="publicaciones/imagenes/", blank=False, max_length=100
    )
    fecha_creacion = models.DateField(default=timezone.now)

    # Relacion Many-to-Many: Una publicación puede tener muchas categorías.
    categorias = models.ManyToManyField(
        Categoria, related_name="publicaciones", blank=True,
    )
    # TODO(Hector Bonilla): Considerar tambien un modelo PublicacionCategoria si
    # se quiere escalar el proyecto.

    def __str__(self) -> str:
        return self.titulo
