from django import forms
from .models import Estudiante


class EstudianteForm(forms.ModelForm):

    fecha_validez = forms.DateField(
        label='Fecha de Validez',
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
        }, format='%Y-%m-%d'),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Estudiante
        fields = ['nombre', 'identificacion', 'carrera', 'foto', 'activo', 'fecha_validez']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'identificacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de identificación'
            }),
            'carrera': forms.Select(attrs={
                'class': 'form-control',
            }),
            'foto': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'activo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'identificacion': 'Identificación',
            'carrera': 'Carrera',
            'foto': 'Foto del Estudiante',
            'activo': 'Carnet Activo',
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Usuario'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
    )
