from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class producto(models.Model):

    class GeneroPerfume(models.TextChoices):
        HOMBRE = "HOMBRE", "Hombre"
        MUJER = "MUJER", "Mujer"
        UNISEX = "UNISEX", "Unisex"
    
    class FormaPerfume(models.TextChoices):
        Cilindro = "Cilindro", "Cilindro"
        Cintura = "Cintura", "Cintura"
        Cuadrado = "Cuadrado", "Cuadrado"
        Esfera = "Esfera", "Esfera"
        Figura = "Figura", "Figura"
        Pack = "Pack", "Pack"
        Prisma = "Prisma", "Prisma"
        Rectangulo = "Rectangulo", "Rectangulo"
        Tronco = "Tronco", "Tronco"

    genero = models.CharField(
        max_length = 20,
        choices=GeneroPerfume.choices,
        default=GeneroPerfume.UNISEX
    )
    nombre = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='nombre')
    descripcion = models.CharField(max_length=400)
    marca = models.CharField(max_length=100)
    contenido_neto = models.IntegerField()
    familia_olfativa = models.CharField(max_length=100)
    notas_salida = models.CharField(max_length=100)
    notas_corazon = models.CharField(max_length=100)
    notas_fondo = models.CharField(max_length=100)
    imagen = models.URLField()
    forma = models.CharField(
        max_length = 20,
        choices=FormaPerfume.choices,
        default=FormaPerfume.Figura
    )
    views = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre}, {self.marca}, {self.genero}, {self.contenido_neto}"

class comentario(models.Model):
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    puntuacion = models.IntegerField(
        default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)]
     )
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Comentario de {self.usuario.username}"

class tiendaOnline(models.Model):
    nombre = models.CharField(max_length=100)
    webScraping_tag = models.CharField(max_length=100)
    webScraping_precio = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.nombre}"

class precio(models.Model):
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    tienda = models.ForeignKey(tiendaOnline, on_delete=models.CASCADE)
    webScraping_url = models.URLField()
    valor = models.IntegerField(null=True, default=0)

    def __str__(self):
        return f"{self.producto.nombre}: {self.tienda.nombre} ${self.valor}"

class registroHistoricoPrecio(models.Model):
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    tienda = models.ForeignKey(tiendaOnline, on_delete=models.CASCADE)
    precio_registrado = models.IntegerField()
    fecha_cambio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto.nombre}, ${self.precio_registrado} en {self.fecha_cambio}"