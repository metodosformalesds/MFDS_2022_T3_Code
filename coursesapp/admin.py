from django.contrib import admin

# Register your models here.
from .models import *

from .models import Perfil, Courses

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'pais','avatar')

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')