# rea_api/forms.py - CÓDIGO FINAL

from django import forms
from .models import Recurso
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm # <-- ¡IMPORTACIÓN NECESARIA!

# Obtener el modelo de usuario personalizado
CustomUser = get_user_model() 

# ---------------------------------------------------
# FORMULARIO DE RECURSO 
# ---------------------------------------------------
class RecursoForm(forms.ModelForm):
    archivo_pdf = forms.FileField(
        required=False,
        label='Subir PDF',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'})
    )

    class Meta:
        model = Recurso
        fields = [
            'titulo',
            'descripcion',
            'idioma',
            'licencia',
            'nivel',
            'categoria',
            'etiquetas'
        ] 
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'idioma': forms.TextInput(attrs={'class': 'form-control'}),
            'licencia': forms.Select(attrs={'class': 'form-select'}),
            'nivel': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'etiquetas': forms.CheckboxSelectMultiple(),
        }


# ---------------------------------------------------
# FORMULARIO DE REGISTRO (LA CLASE QUE FALTABA)
# ---------------------------------------------------
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        # 🚨 VOLVEMOS A INCLUIR 'email' y 'rol' aquí.
        # Asegúrate de que email y rol sean campos válidos en tu CustomUser.
        fields = UserCreationForm.Meta.fields + ('email', 'rol',)