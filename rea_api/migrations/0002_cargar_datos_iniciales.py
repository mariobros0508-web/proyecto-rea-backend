from django.db import migrations

def cargar_datos_rea(apps, schema_editor):
    # ✅ USAMOS 'rea_api' QUE ES EL NOMBRE REAL DE TU APP
    Licencia = apps.get_model('rea_api', 'Licencia')
    NivelEducativo = apps.get_model('rea_api', 'NivelEducativo')
    Categoria = apps.get_model('rea_api', 'Categoria')

    # 1. Crear Licencias
    Licencia.objects.get_or_create(nombre="Dominio Público (CC0)", url_legal="https://creativecommons.org/")
    Licencia.objects.get_or_create(nombre="Creative Commons BY", url_legal="https://creativecommons.org/")
    Licencia.objects.get_or_create(nombre="Copyright", url_legal="https://copyright.gov")

    # 2. Crear Niveles
    NivelEducativo.objects.get_or_create(nombre="Educación Primaria")
    NivelEducativo.objects.get_or_create(nombre="Educación Secundaria")
    NivelEducativo.objects.get_or_create(nombre="Educación Superior")

    # 3. Crear Categorías
    Categoria.objects.get_or_create(nombre="Matemáticas")
    Categoria.objects.get_or_create(nombre="Programación")
    Categoria.objects.get_or_create(nombre="Ciencias Sociales")

class Migration(migrations.Migration):
    dependencies = [
        # ✅ CAMBIADO A 'rea_api' PARA QUE COINCIDA CON TU PROYECTO
        ('rea_api', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(cargar_datos_rea),
    ]
