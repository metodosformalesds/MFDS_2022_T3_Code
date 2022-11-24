"""
Este archivo contiene los formularios creados para el registro
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Skills, Comment
from django.contrib.auth import get_user_model

from django import forms

class CreateUserForm(UserCreationForm): #Se define el formulario de registro
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "CreateUserForm" que servirá para crear un formulario. Este formulario utiliza el modelo USER y almacena las variables "username, email, password1 y password2"
    '''    
    class Meta:
        model = User #Se utiliza el modelo de Usuario ya predefinido de la base de datos
        fields = ['username', 'email', 'password1', 'password2'] #Se ingresan las variables a utilizar en el formulario de registro

class UpdateUserFormAvatar(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "UpdateUserFormAvatar" que servirá para crear un formulario. Este formulario utiliza el modelo PERFIL y almacena la variable "avatar"
    '''
    class Meta:
        model = Perfil
        fields = ['avatar']

class UpdateProfileForm(forms.ModelForm): #Se define el formulario de registro
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "UpdateProfileForm" que servirá para crear un formulario. Este formulario utiliza el modelo PERFIL y almacena la variable "pais"
    '''
    class Meta:
        model = Perfil #Se utiliza el modelo de Usuario ya predefinido de la base de datos
        fields = ['pais'] #Se ingresan las variables a utilizar en el formulario de registro

class UpdateUserForm(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "UpdateUserForm" que servirá para crear un formulario. Este formulario utiliza el modelo USER y almacena las variables "first_name y last_name"
    '''
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UpdateUserFormEmail(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "UpdateUserFormEmail" que servirá para crear un formulario. Este formulario utiliza el modelo USER y almacena la variable "email"
    '''
    class Meta:
        model = User
        fields = ['email']

from django.contrib.auth.forms import SetPasswordForm

class SetPasswordForm(SetPasswordForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "SetPasswordForm" que servirá para crear un formulario. Este formulario utiliza el modelo USER y almacena la variable "new_password1 y new_password2"
    '''
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

#SoftSkills
class SoftSkill1_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "SoftSkill1_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "soft_skill1"
    '''
    class Meta:
        model = Skills
        fields = ['soft_skill1']

class SoftSkill2_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "SoftSkill2_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "soft_skill2"
    '''
    class Meta:
        model = Skills
        fields = ['soft_skill2']

class SoftSkill3_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "SoftSkill3_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "soft_skill3"
    '''
    class Meta:
        model = Skills
        fields = ['soft_skill3']

class SoftSkill4_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "SoftSkill4_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "soft_skill4"
    '''
    class Meta:
        model = Skills
        fields = ['soft_skill4']

class SoftSkill5_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "SoftSkill5_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "soft_skill5"
    '''
    class Meta:
        model = Skills
        fields = ['soft_skill5']



#HardSkills
class HardSkill1_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "HardSkill1_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "hard_skill1"
    '''
    class Meta:
        model = Skills
        fields = ['hard_skill1']

class HardSkill2_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "HardSkill2_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "hard_skill2"
    '''
    class Meta:
        model = Skills
        fields = ['hard_skill2']

class HardSkill3_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "HardSkill3_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "hard_skill3"
    '''
    class Meta:
        model = Skills
        fields = ['hard_skill3']

class HardSkill4_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "HardSkill4_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "hard_skill4"
    '''
    class Meta:
        model = Skills
        fields = ['hard_skill4']

class HardSkill5_form(forms.ModelForm):
    '''
    Por Cinthia Elena Hernández Rodríguez
    Creación de la clase "HardSkill5_form" que servirá para crear un formulario. Este formulario utiliza el modelo SKILLS y almacena la variable "hard_skill5"
    '''
    class Meta:
        model = Skills
        fields = ['hard_skill5']


class addCommentForm(forms.ModelForm):

    class Meta: 
        model = Comment
        fields = ['comment']