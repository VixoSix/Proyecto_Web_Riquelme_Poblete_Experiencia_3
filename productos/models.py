import datetime
from django.db import models
from distutils.command.upload import upload
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.


class Envoltura(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name='Id de categoria')
    nombreCategoria = models.CharField(max_length=50, verbose_name='Nombre de categoria')

    def __str__(self):
        return self.nombreCategoria


class Roll(models.Model):
    idRool = models.IntegerField(primary_key=True, verbose_name='Id de roll')
    nombreRool = models.CharField(max_length=255, verbose_name='Nombre de roll')
    descripcionRool=models.CharField(max_length=255, verbose_name='Descripcion')
    stockRoll=models.IntegerField()
    imagenRool = models.ImageField(upload_to="imagenes", null=True, verbose_name='Imagen de roll')
    precioRoll = models.IntegerField(blank=True, null=True, verbose_name='Precio del roll')
    Envoltura = models.ForeignKey('Envoltura', default=1, on_delete=models.CASCADE, verbose_name='Envoltura')

    def __str__(self):
        return self.nombreRool

class Boleta(models.Model):
    id_boleta=models.AutoField(primary_key=True)
    total=models.BigIntegerField()
    impuestos = models.BigIntegerField(default=0)
    envio = models.BigIntegerField(default=0)
    fechaCompra=models.DateTimeField(blank=False, null=False, default = datetime.datetime.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id_boleta)

class detalle_boleta(models.Model):
    id_boleta = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Roll', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)