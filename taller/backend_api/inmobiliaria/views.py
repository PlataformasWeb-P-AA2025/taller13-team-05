from django.shortcuts import render
# Create your views here.
# backend_api/inmobiliaria/views.py
from rest_framework import viewsets, permissions 
from .models import Edificio, Departamento
from .serializers import EdificioSerializer, DepartamentoSerializer

class EdificioViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar edificios.
    """
    queryset = Edificio.objects.all()
    serializer_class = EdificioSerializer
    permission_classes = [permissions.IsAuthenticated] 


class DepartamentoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver y editar departamentos.
    """
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [permissions.IsAuthenticated]