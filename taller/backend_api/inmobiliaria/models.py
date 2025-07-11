# backend_api/inmobiliaria/models.py
from django.db import models

class Edificio(models.Model):
    """
    Define la estructura de un Edificio.
    """
    TIPO_EDIFICIO_CHOICES = [
        ('residencial', 'Residencial'),
        ('comercial', 'Comercial'),
    ]

    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    ciudad = models.CharField(max_length=50)
    tipo = models.CharField(max_length=30, choices=TIPO_EDIFICIO_CHOICES)

    def __str__(self):
        """
        Representación en cadena del modelo, útil para el admin de Django.
        """
        return f"{self.nombre} ({self.tipo}) - {self.ciudad}"

class Departamento(models.Model):
    """
    Define la estructura de un Departamento, que pertenece a un Edificio.
    """
    propietario = models.CharField(max_length=100, verbose_name="Nombre completo del propietario")
    costo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Costo del departamento")
    num_cuartos = models.IntegerField(verbose_name="Número de cuartos")
    
    # La relación clave: un Departamento pertenece a un Edificio.
    edificio = models.ForeignKey(Edificio, on_delete=models.CASCADE, related_name="departamentos")

    def __str__(self):
        """
        Representación en cadena del modelo.
        """
        return f"Dpto. de {self.propietario} - {self.edificio.nombre}"