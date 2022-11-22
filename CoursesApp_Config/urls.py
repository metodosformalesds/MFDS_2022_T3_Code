"""CoursesApp_Config URL Configuration
Lista urlpatterns: Lista ordenada cuyos elementos es cada una de las URL que tendrá nuestro
sitio web. Para este caso se hace uso de la función "include" que nos permitirá incluir en nustro
urlpatterns las URL que se encuentran dentro de "CoursesApp".


"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls), #URL del administrador de Django,
    path('', include('coursesapp.urls')), #El método include nos indica que importaremos las URL de "coursesapp.url" a este archivo
    
]
