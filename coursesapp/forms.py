"""
Este archivo contiene los formularios creados para el registro
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil

from django import forms

class CreateUserForm(UserCreationForm): #Se define el formulario de registro
	class Meta:
		model = User #Se utiliza el modelo de Usuario ya predefinido de la base de datos
		fields = ['username', 'email', 'password1', 'password2'] #Se ingresan las variables a utilizar en el formulario de registro

class UpdateUserFormAvatar(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ['avatar']