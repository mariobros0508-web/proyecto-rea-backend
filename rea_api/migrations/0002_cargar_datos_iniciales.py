from django.db import migrations

def cargar_datos_rea(apps, schema_editor):
    # Obtenemos los modelos
    Licencia = apps.get_model('recursos', 'Licencia')
    NivelEducativo = apps.get_model('recursos', 'NivelEducativo')
    Categoria = apps.get_model('recursos', 'Categoria')

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
        ('recursos', '0001_initial'), # Revisa que el nombre del archivo 0001 sea exacto
    ]

    operations = [
        migrations.RunPython(cargar_datos_rea),
    ]
