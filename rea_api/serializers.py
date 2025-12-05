from rest_framework import serializers
# 1. CORRECCIÓN: Importar CustomUser en lugar de Usuario
from .models import Recurso, Licencia, NivelEducativo, Categoria, CustomUser, Etiqueta

# --- Serializadores de Tablas de Soporte ---

class LicenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Licencia
        fields = '__all__'

class NivelEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NivelEducativo
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

# 2. CORRECCIÓN: Serializador del Usuario Principal (CustomUser)
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        # Apunta al modelo de usuario principal
        model = CustomUser 
        # Es buena práctica limitar los campos serializados por seguridad
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'rol') 

class EtiquetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etiqueta
        fields = '__all__'

# --- Serializador Principal ---

class RecursoSerializer(serializers.ModelSerializer):
    licencia = LicenciaSerializer()
    nivel = NivelEducativoSerializer()
    categoria = CategoriaSerializer()
    
    # 3. CORRECCIÓN: Usa el nuevo CustomUserSerializer
    curador = CustomUserSerializer() 
    
    etiquetas = EtiquetaSerializer(many=True)

    class Meta:
        model = Recurso
        fields = '__all__'