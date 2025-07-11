# backend_api/inmobiliaria/admin.py

from django.contrib import admin
from .models import Edificio, Departamento

class EdificioAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Edificio.
    """
    list_display = ('nombre', 'ciudad', 'tipo')
    search_fields = ('nombre', 'ciudad')

admin.site.register(Edificio, EdificioAdmin)


class DepartamentoAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Departamento.
    """
    list_display = ('propietario', 'costo', 'num_cuartos', 'edificio')
    search_fields = ('propietario', 'edificio__nombre') # Permite buscar por nombre del propietario o del edificio
    raw_id_fields = ('edificio',)

admin.site.register(Departamento, DepartamentoAdmin)