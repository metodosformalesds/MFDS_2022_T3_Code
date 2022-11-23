"""
Este archivo contiene los formularios creados para el registro
"""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Skills
from django.contrib.auth import get_user_model

from django import forms

class CreateUserForm(UserCreationForm): #Se define el formulario de registro
	class Meta:
		model = User #Se utiliza el modelo de Usuario ya predefinido de la base de datos
		fields = ['username', 'email', 'password1', 'password2'] #Se ingresan las variables a utilizar en el formulario de registro

class UpdateUserFormAvatar(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ['avatar']

class UpdateProfileForm(forms.ModelForm): #Se define el formulario de registro
	class Meta:
		model = Perfil #Se utiliza el modelo de Usuario ya predefinido de la base de datos
		fields = ['pais'] #Se ingresan las variables a utilizar en el formulario de registro

class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class UpdateUserFormEmail(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']

from django.contrib.auth.forms import SetPasswordForm

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

#SoftSkills
class SoftSkill1_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['soft_skill1']

class SoftSkill2_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['soft_skill2']

class SoftSkill3_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['soft_skill3']

class SoftSkill4_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['soft_skill4']

class SoftSkill5_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['soft_skill5']



#HardSkills
class HardSkill1_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['hard_skill1']

class HardSkill2_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['hard_skill2']

class HardSkill3_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['hard_skill3']

class HardSkill4_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['hard_skill4']

class HardSkill5_form(forms.ModelForm):

    class Meta:
        model = Skills
        fields = ['hard_skill5']