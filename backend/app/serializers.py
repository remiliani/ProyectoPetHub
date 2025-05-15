from rest_framework import serializers
from .models import Cliente, Mascota, Cita

class ClienteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    

class MascotaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField(max_length=255)
    especie = serializers.CharField(max_length=255)
    edad = serializers.IntegerField()
    

class CitaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    fecha = serializers.DateTimeField()
    motivo = serializers.CharField(max_length=255)
    