from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import os

# 1. LICENCIA
class Licencia(models.Model):
    licencia_id = models.AutoField(primary_key=True) 
    
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    url_legal = models.URLField(max_length=255)

    class Meta:
        db_table = 'licencia' 

    def __str__(self):
        return self.nombre

# 2. NIVEL EDUCATIVO
class NivelEducativo(models.Model):
    nivel_id = models.AutoField(primary_key=True) 
    
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'nivel_educativo' 

    def __str__(self):
        return self.nombre

# 3. CATEGORIA
class Categoria(models.Model):
    categoria_id = models.AutoField(primary_key=True)
    
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'categoria' 

    def __str__(self):
        return self.nombre

# 4. ETIQUETA
class Etiqueta(models.Model):
    etiqueta_id = models.AutoField(primary_key=True)
    
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'etiqueta' 

    def __str__(self):
        return self.nombre

# 5. USUARIO
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('curador', 'Curador'),
        ('usuario', 'Usuario'),
    ]

    rol = models.CharField(max_length=10, choices=ROLE_CHOICES, default='usuario')
    
    # ... otros campos si son necesarios y no están en AbstractUser
    # Por ejemplo, si tenías un campo de fecha_registro que quieres mantener,
    # aunque AbstractUser ya maneja date_joined.

    class Meta:
        db_table = 'custom_user'
        # ...

# 6. RECURSO
class Recurso(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    
    # ✅ Ahora el campo es opcional (no exige URL si se sube un PDF)
    url_acceso = models.URLField(blank=True, null=True)
    
    idioma = models.CharField(max_length=50)
    licencia = models.ForeignKey('Licencia', on_delete=models.SET_NULL, null=True)
    nivel = models.ForeignKey('NivelEducativo', on_delete=models.SET_NULL, null=True)
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True)
    
    # Curador que sube el recurso (usuario)
    curador = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recursos_creados'
    )

    # Relación ManyToMany con etiquetas opcionales
    etiquetas = models.ManyToManyField('Etiqueta', blank=True)
    activo = models.BooleanField(default=True)
    # Fecha automática de subida
    fecha_subida = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo

# 7. RECURSO_ETIQUETA (M:N)
class RecursoEtiqueta(models.Model):
    recurso = models.ForeignKey('Recurso', on_delete=models.CASCADE)
    etiqueta = models.ForeignKey('Etiqueta', on_delete=models.CASCADE)

    class Meta:
        db_table = 'recurso_etiqueta'
        unique_together = ('recurso', 'etiqueta')  # combinación única

    def __str__(self):
        return f"{self.recurso.titulo} - {self.etiqueta.nombre}"