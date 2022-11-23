from django.contrib import admin

# Register your models here.
from .models import *

from .models import Perfil, Curso

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'pais','avatar')

@admin.register(Curso)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


