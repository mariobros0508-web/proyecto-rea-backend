from django.urls import path
from . import views

urlpatterns = [
    # --- CRUD Recursos ---
    path('', views.recurso_list, name='recurso_list'),
    path('recurso/nuevo/', views.recurso_nuevo, name='recurso_nuevo'), # La vista se llama recurso_nuevo
    path('recurso/<int:pk>/', views.recurso_detail, name='recurso_detail'),
    path('recurso/<int:pk>/editar/', views.recurso_update, name='recurso_update'),
    path('recurso/<int:pk>/eliminar/', views.recurso_eliminar, name='recurso_eliminar'),

    # --- Autenticación ---
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    # --- Dashboard ---
    path('dashboard/', views.curador_dashboard, name='dashboard'),

    # --- API JSON ---
    path('api/recursos/', views.api_recursos_list, name='api_recursos_list'),
    path('api/recursos/<int:pk>/', views.api_recurso_detail, name='api_recurso_detail'),
    path('api/recursos/nuevo/', views.api_recurso_create, name='api_recurso_create'),
    path('api/externos/search/', views.BusquedaExternaAPIView.as_view(), name='busqueda_externa_api'),
]
