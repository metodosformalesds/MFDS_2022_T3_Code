from django.contrib import admin

# Register your models here.
from .models import *

from .models import Perfil, Curso, Skills

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills', 'pais','avatar')

@admin.register(Curso)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

@admin.register(Skills)
class SkillsAdmin(admin.ModelAdmin):
    list_display = ('user', 'soft_skill1', 'soft_skill2', 'soft_skill3', 'soft_skill4', 'soft_skill5', 'hard_skill1', 'hard_skill2', 'hard_skill3', 'hard_skill4', 'hard_skill5')
