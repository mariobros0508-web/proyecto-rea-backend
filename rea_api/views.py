# rea_api/views.py - CÓDIGO CORREGIDO

import os
import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test  
from django.contrib import messages
from .models import Recurso, CustomUser
from .forms import RecursoForm, CustomUserCreationForm # <-- ¡NUEVA IMPORTACIÓN!
from rest_framework.views import APIView
from rest_framework.response import Response

# -------------------------------------------------
# FUNCIONES DE CONTROL DE ROLES
# -------------------------------------------------
def es_admin(user):
    # Comprueba si el usuario está logueado Y si el campo 'rol' es 'admin'
    return user.is_authenticated and user.rol == 'admin' 

def es_curador(user):
    # Comprueba si el usuario está logueado Y si el campo 'rol' es 'curador' O 'admin'
    return user.is_authenticated and user.rol in ['curador', 'admin']


# -------------------------------------------------
# CRUD DE RECURSOS (HTML)
# -------------------------------------------------
def recurso_list(request):
    recursos = Recurso.objects.all().order_by('-fecha_subida')
    return render(request, 'rea_api/recurso_list.html', {'recursos': recursos})


def recurso_detail(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    return render(request, 'rea_api/recurso_detail.html', {'recurso': recurso})


@user_passes_test(es_curador)
def recurso_nuevo(request):
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES)
        if form.is_valid():
            recurso = form.save(commit=False)
            recurso.curador = request.user  # 🔹 Asigna el usuario autenticado
            recurso.save()
            messages.success(request, '✅ Recurso creado correctamente.')
            return redirect('recurso_list')
        else:
            messages.error(request, f'❌ Errores del formulario: {form.errors}')
    else:
        form = RecursoForm()

    return render(request, 'rea_api/recurso_form.html', {
        'form': form,
        'titulo_form': 'Agregar Nuevo Recurso',
    })


@user_passes_test(es_curador)
def recurso_update(request, pk):
    recurso = get_object_or_404(Recurso, pk=pk)
    if request.method == 'POST':
        form = RecursoForm(request.POST, request.FILES, instance=recurso)
        archivo_pdf = request.FILES.get('archivo_pdf')

        if form.is_valid():
            recurso = form.save(commit=False)

            # Si se sube un nuevo PDF, reemplaza el anterior
            if archivo_pdf:
                pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', archivo_pdf.name)
                os.makedirs(os.path.dirname(pdf_path), exist_ok=True)
                with open(pdf_path, 'wb+') as destino:
                    for chunk in archivo_pdf.chunks():
                        destino.write(chunk)
                recurso.url_acceso = f"/media/pdfs/{archivo_pdf.name}"

            recurso.save()
            messages.success(request, '✅ Recurso actualizado correctamente.')
            return redirect('recurso_list')
        else:
            messages.error(request, f'❌ Errores del formulario: {form.errors}')
    else:
        form = RecursoForm(instance=recurso)

    return render(request, 'rea_api/recurso_form.html', {'form': form, 'titulo_form': 'Editar Recurso'})


@user_passes_test(es_admin)
def recurso_eliminar(request, pk):  # 🔹 Nombre cambiado para coincidir con urls.py
    recurso = get_object_or_404(Recurso, pk=pk)

    if request.user == recurso.curador or request.user.is_superuser:
        recurso.delete()
        messages.success(request, '🗑️ Recurso eliminado correctamente.')
    else:
        messages.error(request, '🚫 No tienes permiso para eliminar este recurso.')

    return redirect('recurso_list')


# -------------------------------------------------
# API JSON (Django REST Framework)
# -------------------------------------------------
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecursoSerializer


@api_view(['GET'])
def api_recursos_list(request):
    recursos = Recurso.objects.all()
    serializer = RecursoSerializer(recursos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_recurso_detail(request, pk):
    try:
        recurso = Recurso.objects.get(pk=pk)
    except Recurso.DoesNotExist:
        return Response({'error': 'Recurso no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    serializer = RecursoSerializer(recurso)
    return Response(serializer.data)


@api_view(['POST'])
def api_recurso_create(request):
    serializer = RecursoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -------------------------------------------------
# CONTROL DE USUARIOS (LOGIN, REGISTRO, LOGOUT)
# -------------------------------------------------
# rea_api/views.py - MODIFICACIÓN DENTRO DE register_view

# ... otras funciones ...

# -------------------------------------------------
# CONTROL DE USUARIOS (LOGIN, REGISTRO, LOGOUT)
# -------------------------------------------------
# rea_api/views.py - CÓDIGO CORREGIDO PARA register_view

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST) 
        if form.is_valid():
            # 🚨 Si incluyes 'rol' en forms.py, usa form.save()
            form.save()
            messages.success(request, 'Registro exitoso. Por favor, inicia sesión.')
            return redirect('login')
        else:
            # Si POST es inválido, el código continúa para mostrar el formulario con errores
            print("ERRORES DEL FORMULARIO:", form.errors)
            messages.error(request, 'Error en el formulario de registro. Revise los campos.')
    else: # ⬅️ Este bloque maneja la solicitud GET
        form = CustomUserCreationForm() # Crea un formulario vacío para el GET

    # 🚨 LA LÍNEA MÁS IMPORTANTE: Esto asegura que SIEMPRE se devuelve una respuesta
    return render(request, 'rea_api/register.html', {'form': form, 'titulo_form': 'Registrar Nuevo Usuario'})

        # ...
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('recurso_list')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')

    return render(request, 'rea_api/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect('login')


# -------------------------------------------------
# DASHBOARD DEL CURADOR (solo usuarios logueados)
# -------------------------------------------------
@login_required(login_url='login')
def curador_dashboard(request):
    return render(request, 'rea_api/dashboard.html', {'user': request.user})

# rea_api/views.py - Insertar ESTE BLOQUE COMPLETO

# ... (Después de api_recurso_create) ...

# -------------------------------------------------
# API EXTERNA (PROXY) - ¡BLOQUE FALTANTE!
# -------------------------------------------------
class BusquedaExternaAPIView(APIView):
    """
    API Proxy que busca libros en el Proyecto Gutenberg (repositorio OER)
    y devuelve los resultados como JSON.
    """
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({"error": "Parámetro 'q' (consulta) es requerido para la búsqueda externa."}, status=400)

        URL_EXTERNA = 'http://gutendex.com/books/'
        
        params = {
            'search': query,
            'limit': 10
        }

        try:
            # Realizar la solicitud HTTP al API externo
            response = requests.get(URL_EXTERNA, params=params, timeout=10)
            response.raise_for_status() 

            datos_externos = response.json()
            
            # Devolver los datos del API externo directamente al cliente
            return Response(datos_externos)
            
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión: {e}")
            return Response(
                {"error": "No se pudo conectar con el repositorio externo. Intente más tarde.", "detalle": str(e)}, 
                status=503
            )

# -------------------------------------------------
# CONTROL DE USUARIOS (LOGIN, REGISTRO, LOGOUT)
# -------------------------------------------------
# ... (continúa el resto de tu views.py) ...