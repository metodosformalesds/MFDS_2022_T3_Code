"""
El archivo url.py será el encargado de mandarle a urls.py dentro de CoursesAppConfig esta lista de urlpatterns para que maneje las URL de la página web
"""
from django.urls import path #Utilizamos la funcion path para guardar la dirección de las vistas
from . import views # se importa el archivo views

urlpatterns = [
	path('register/', views.registerPage, name="register"), # Se crea la URL de registro que tendrá lo que la view RegisterPage
	path('login/', views.loginPage, name="login"),  #Se crea la URL de login que tendrá lo que la view LoginPage
	path('logout/', views.logoutUser, name="logout"), 

    path('', views.home, name="home") #Se crea la URL de home que tendrá lo que la view home


]