"""Modelo de la aplicación de publicaciones.

Define los modelos `Categoria` y `Publicacion` utilizados para representar 
los datos de la plataforma de compra y venta de la FCFM.

La relación entre ambos modelos es Many-to-many:
- Una publicación puede pertenecer a muchas categorías.
- Una categoría puede agrupar muchas publicaciones o no tener alguna publicación.

Ante cualquier cambio a estos modelos, recordar ejecutar:
    $ python manage.py makemigrations
    $ python manage.py migrate

"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator



class Categoria(models.Model):
    """ Representa una categoría temática para clasificar las publicaciones.
    
    Ejemplos de categorías: Comida, Clases particulares, Ropa, Mueebles, Arriendos, etc.

    Attributes:
        nombre: Nombre descriptivo de la categoría (máximo 64 caracteres).
    
    """
    nombre = models.CharField(max_length=64)

    def __str__(self) -> str:
        """Retorna el nombre de la categoría convirtiendo un objeto a texto comprensible para el usuario."""
        return self.nombre


class Publicacion(models.Model):
    """ Representa un producto publicado en la págin web.

    Cada publicación corresponde a un producto o servicio que un integrante de la facultad desea vender. 
    Incluye título, imagen, descripción, fecha de creación (se genera automáticamente) y puede estar asociada 
    a una o más categorías.

    Attributes:
        titulo: Título único que identifica el producto o servicio (máximo 128 caracteres).
        descripcion: Descripción detallada de las características del producto o servicio, precio, forma de entrega, etc.
        imagen: foto del producto o servicio, almacenada en 'publicaciones/imagenes/'.
        fecha_creacion: fecha en que se creó la publicación (se asigna automáticamente).
        categorias: Categorías asociadas al producto o servicio.

    Note:
         TODO(Hector Bonilla): Considerar tambien un modelo intermedio PublicacionCategoria si
         se quiere escalar el proyecto.

    """
    
    ESTADOS_DISPONIBILIDAD = [
        ("DISPONIBLE", "Disponible"),
        ("RESERVADO", "Reservado"),
        ("NO_DISPONIBLE", "No disponible"),
    ]
    # Título visible del producto o servicio
    titulo = models.CharField(max_length=128, blank=False, validators= [MinLengthValidator(3)])

    # Descripción completa del producto o servicio: características generales, estado, forma de entrega, etc
    descripcion = models.TextField(blank=False)
    
    # La imagen se guarda en MEDIA_ROOT/publicaciones/imagenes/
    imagen = models.ImageField(
        upload_to="publicaciones/imagenes/", blank=False, max_length=100
    )

    #Muestra precio del producto 
    precio = models.PositiveIntegerField()

    # Muestra ubicación del producto/servicio ofrecido
    ubicacion = models.CharField(max_length=128)

    #Disponibilidad del producto o servicio
    disponibilidad = models.CharField(max_length=20, choices=ESTADOS_DISPONIBILIDAD, default="DISPONIBLE")
   
   #Muestra el nombre del vendedor del producto/servicio
    nombre_vendedor = models.CharField(max_length=128)
    
    #Correo de contacto del vendedor
    correo_electronico = models.EmailField()

    #Teléfono de contacto del vendedor
    telefono = models.CharField(max_length=12)

    # Se asigna la fecha del momento en el que se crea la publicación
    fecha_creacion = models.DateField(default=timezone.now)

    # Relacion Many-to-Many: Una publicación puede tener varias categorías y una categoría puede tener
    # varias publicaciones o ninguna publicación.
    # blank=True permite que una publicación no tenga categorías asignadas, y que una categoría exista
    # sin publicaciones asociadas.
    categorias = models.ManyToManyField(
        Categoria, related_name="publicaciones",
    )


    def __str__(self) -> str:
        """ Retorna el título de la publicación convirtiendo el objeto a texto comprensible para el usuario."""
        return self.titulo
