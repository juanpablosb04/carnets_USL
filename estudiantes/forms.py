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
        fields = ['nombre', 'identificacion', 'carrera', 'foto', 'fecha_validez']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo'
            }),
            'identificacion': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Número de identificación',
            'inputmode': 'numeric',
            'pattern': '[0-9]*',
            'oninput': 'this.value = this.value.replace(/[^0-9]/g, "")'
            }),
            'carrera': forms.Select(attrs={
                'class': 'form-control',
            }),
            'foto': forms.FileInput(attrs={
            'class': 'file-input-hidden',
            'accept': 'image/*'
            }),
        }
        labels = {
            'nombre': 'Nombre Completo',
            'identificacion': 'Identificación',
            'carrera': 'Carrera',
            'foto': 'Foto del Estudiante',
            'activo': 'Carnet Activo',
        }

def clean_identificacion(self):
    data = self.cleaned_data.get('identificacion', '')

    if not data.isdigit():
        raise forms.ValidationError("Solo se permiten números.")

    if Estudiante.objects.filter(identificacion=data).exclude(pk=self.instance.pk).exists():
        raise forms.ValidationError("Esta identificación ya existe.")

    return data

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
