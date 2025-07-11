# backend_api/inmobiliaria/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EdificioViewSet, DepartamentoViewSet

# Crea un router y registra nuestros viewsets
router = DefaultRouter()
router.register(r'edificios', EdificioViewSet, basename='edificio')
router.register(r'departamentos', DepartamentoViewSet, basename='departamento')

# Las URLs de la API son determinadas automáticamente por el router.
urlpatterns = [
    path('', include(router.urls)),
]