from django import forms 
from django.forms import ModelForm
from django.forms import widgets
from django.forms.widgets import Widget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Envoltura, Roll

class RollForm(forms.ModelForm):
    class Meta: 
        model=Roll
        fields=['idRool', 'nombreRool', 'descripcionRool', 'stockRoll', 'imagenRool','precioRoll','Envoltura']
        labels={
            'idRool': 'Id de roll',
            'nombreRool': 'Nombre de roll',
            'descripcionRool': 'Descripcion',
            'stockRoll': 'stock',
            'imagenRool': 'Imagen de roll',
            'precioRoll':'Precio del roll',
            'Envoltura':'Envoltura'
        }
        widgets={
            'idRool': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese Id Roll',
                    'id':'idRool'
                }
            ),
            'nombreRool': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese el nombre',
                    'id':'nombreRool'
                }
            ),
            'descripcionRool': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese una descripcion',
                    'id':'descripcionRool'
                }
            ),
            'stockRoll': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese el stock',
                    'id':'stockRoll'
                }
            ),
            'imagenRool': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id':'imagenRool'
                }
            ),
            'precioRoll': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder':'Ingrese el precio',
                    'id':'precioRoll'
                }
            ),
            'Envoltura': forms.Select(
                attrs={
                    'class': 'form-control',
                    'id':'Envoltura'
                }
            )
        }

class RegistroUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class MetodoEntregaForm(forms.Form):
    METODOS_ENTREGA = [
        ('envio', 'Envío a domicilio'),
        ('retiro', 'Retiro en tienda'),
    ]
    metodo_entrega = forms.ChoiceField(choices=METODOS_ENTREGA, widget=forms.RadioSelect)