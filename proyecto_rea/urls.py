"""
URL configuration for proyecto_rea project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# proyecto_rea/urls.py (al inicio)
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views # Importar vistas de autenticación de Django
from rea_api import views as rea_views # Importar tus vistas
# Importar settings y static para servir media files en desarrollo
from django.conf import settings 
from django.conf.urls.static import static

# proyecto_rea/urls.py

urlpatterns = [
    path('admin/', admin.site.urls),

    # ----------------- VISTAS DE AUTENTICACIÓN -----------------
    # Login (Usa la vista integrada de Django, renderizando tu plantilla) [cite: 16]
    path('login/', auth_views.LoginView.as_view(template_name='rea_api/login.html'), name='login'),

    # Logout (Usa la vista integrada de Django) [cite: 16]
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Registro (Usa tu vista personalizada) [cite: 16]
    path('register/', rea_views.register_view, name='register'),

    # Dashboard (Vista Protegida) [cite: 17]
    path('dashboard/', rea_views.curador_dashboard, name='dashboard'),
    # ----------------- FIN VISTAS DE AUTENTICACIÓN -----------------

    path('', include('rea_api.urls')),
]

# Servir archivos media (PDFs) en entorno de desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)