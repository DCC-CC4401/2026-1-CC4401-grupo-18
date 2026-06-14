"""Modelo de la aplicación de publicaciones.

Define los modelos ``Categoria`` y ``Publicacion`` utilizados para representar 
los datos de la plataforma de compra y venta de la FCFM.

La relación entre ambos modelos es Many-to-many:
- Una publicación puede pertenecer a muchas categorías.
- Una categoría puede agrupar muchas publicaciones, o ninguna.

Ante cualquier cambio a estos modelos, recordar ejecutar:
    $ python manage.py makemigrations
    $ python manage.py migrate

"""

from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator



class Categoria(models.Model):
    """ Representa una categoría temática para clasificar las publicaciones.
    
    Ejemplos de categorías: Comida, Clases particulares, Ropa, Muebles, Arriendos, etc.

    Attributes:
        nombre (str): Nombre descriptivo de la categoría (máximo 64 caracteres).
    
    """

    # Nombre de la categoría, visible para el usuario en filtros y formularios.
    nombre = models.CharField(max_length=64)

    def __str__(self) -> str:
        """Retorna el nombre de la categoría como representación legible del objeto."""
        return str(self.nombre)


class Publicacion(models.Model):
    """ Representa un producto o servicio publicado en la página web.

    Cada publicación corresponde a un producto o servicio que un integrante de la facultad desea vender. 
    Incluye información del producto o servicio (titulo, imagen, descripcion, precio, disponibilidad) 
    y datos de contacto del vendedor (nombre_vendedor, ubicacion, correo_electronico y telefono).
    La fecha de creación de la publicación se asigna automáticamente al momento de guardar.

    Attributes:
        titulo (str): Título único que identifica el producto o servicio (entre 3 y 128 caracteres).
        descripcion (str): Descripción detallada del producto o servicio: características, forma de entrega, 
            estado, etc.
        imagen (ImageField): foto del producto o servicio, almacenada en ``MEDIA_ROOT/publicaciones/imagenes/``.
        precio (int): Precio del producto o servicio en pesos chilenos (entero positivo).
        ubicacion (str): Lugar en donde se encuentra el producto o se presta el servicio.
        disponibilidad (str): Estado actual del producto. Dentro de los valores definidos en ``ESTADOS_DISPONIBILIDAD``
            se encuentra: ``NO_DISPONIBLE``, ``RESERVADO`` y por defecto ``DISPONIBLE``.
        nombre_vendedor (str): Nombre completo del vendedor o prestador del servicio.
        correo_electronico (str): Correo electrónico de contacto del vendedor.
        telefono (str): Número de teléfono de contacto del vendedor (máximo 12 caracteres, ej: ``+56912345678``).
        fecha_creacion (date): Fecha en que se creó la publicación (se asigna automáticamente).
        categorias (ManyToManyField): Categorías asociadas al producto o servicio. Una publicación puede no tener
            categorías asignadas (``blank=True``).

    Note:
         TODO(Hector Bonilla): Considerar tambien un modelo intermedio ``PublicacionCategoria`` si
         se quiere escalar el proyecto.

         El campo ``categorias`` tiene ``blank=True``, lo que permite crear publicaciones sin categoría
         desde el panel de administración. La validación que exige al menos una categoría debe aplicarse 
         en el formulario. 
         Ver: ``publicaciones/forms.PublicacionForm.clean``.
    """
    
    ESTADOS_DISPONIBILIDAD = [
        ("DISPONIBLE", "Disponible"),
        ("RESERVADO", "Reservado"),
        ("NO_DISPONIBLE", "No disponible"),
    ]

    # Título visible del producto o servicio. Mínimo 3 caracteres, máximo 128.
    titulo = models.CharField(max_length=128, blank=False, validators= [MinLengthValidator(3)])

    # Descripción completa del producto o servicio: características generales, estado, forma de entrega, etc.
    descripcion = models.TextField(blank=False)
    
    # Imagen que corresponde a la foto del producto o servicio. Se guarda en MEDIA_ROOT/publicaciones/imagenes/
    imagen = models.ImageField(
        upload_to="publicaciones/imagenes/", blank=False, max_length=100
    )

    # Precio del producto o servicio en pesos (entero positivo, sin decimales ni separador de miles).
    precio = models.PositiveIntegerField()

    # Lugar en donde se encuentra el producto o donde se presta el servicio ofrecido (máximo 128 caracteres).
    ubicacion = models.CharField(max_length=128)

    # Estado actual del producto o servicio: DISPONIBLE, RESERVADO o NO_DISPONIBLE.
    disponibilidad = models.CharField(max_length=20, choices=ESTADOS_DISPONIBILIDAD, default="DISPONIBLE")
   
    # Nombre completo del vendedor del producto/servicio (máximo 128 caracteres).
    nombre_vendedor = models.CharField(max_length=128)
    
    # Correo electrónico de contacto del vendedor.
    correo_electronico = models.EmailField()

    # Teléfono de contacto del vendedor (máximo 12 caracteres, ej: +56912345678).
    telefono = models.CharField(max_length=12)

    # Fecha de creación de la publicación. Se asigna automáticamente al confirmar la publicación.
    fecha_creacion = models.DateField(default=timezone.now)

    # Relacion Many-to-Many con Categoria. Ver docstring de la clase Publicacion para explorar detalles sobre blank=True.
    categorias = models.ManyToManyField(
        Categoria, related_name="publicaciones", blank=True,
    )
    # TODO(Hector Bonilla): Ojo con el blank True. Si bien gracias al formulario la base de
    # datos una publicación nunca va a tener una categoría, si se pueden
    # crear por admin una publicación sin categoría. Lo que se podría hacer
    # es que el formulario trate este caso dentro de su programación.
    # -> CompraVentasProject/publicaciones/forms.PublicacionForm.clean()


    def __str__(self) -> str:
        """Retorna el título de la publicación como representación legible del objeto."""
        return str(self.titulo)
