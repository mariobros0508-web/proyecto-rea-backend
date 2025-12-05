from django.contrib import admin
from .models import (
    Licencia, NivelEducativo, Categoria, Etiqueta, 
    Recurso, RecursoEtiqueta, CustomUser 
)

# Registrar los modelos en el panel de administración
admin.site.register(Licencia)
admin.site.register(NivelEducativo)
admin.site.register(Categoria)
admin.site.register(Etiqueta)
admin.site.register(CustomUser)
admin.site.register(Recurso)
admin.site.register(RecursoEtiqueta)
