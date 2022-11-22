"""
El archivo url.py será el encargado de mandarle a urls.py dentro de CoursesAppConfig esta lista de urlpatterns para que maneje las URL de la página web
"""
from django.urls import path #Utilizamos la funcion path para guardar la dirección de las vistas
from . import views # se importa el archivo views
#from .views import profileConfigEmail
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.urls import path, include


urlpatterns = [
	path('register/', views.registerPage, name="register"), # Se crea la URL de registro que tendrá lo que la view RegisterPage
	path('login/', views.loginPage, name="login"),  #Se crea la URL de login que tendrá lo que la view LoginPage
	path('logout/', views.logoutUser, name="logout"), 
	path('profile/', views.profileUser, name='profile'),
	path('profileConfig/', views.profileConfig, name='profileConfig'),
	path('profileConfigAvatar/', views.profileConfigAvatar, name='profileConfigAvatar'),
	path('profileConfigEmail/', views.profileConfigEmail, name='profileConfigEmail'),
	path("profileConfigPassword/", views.password_change, name="profileConfigPassword"),
	path('courses/', views.courses, name='courses'),
	path('courseView/<int:id>', views.courseView, name='courseView'), #Se crea el la URL de la vista para un curso 
	path('courses/<str:category>', views.courses_for_category, name='courses'),		#Filtrado por categorias 
	path('jobs/', views.jobs, name='jobs'),
    path('', views.home, name="home"), #Se crea la URL de home que tendrá lo que la view home
	path('skills/', views.skills, name='skills'),
    path('', views.home, name="home"), #Se crea la URL de home que tendrá lo que la view home

	path('search/', views.searchBar, name='search'), #Barra de búsqueda
	path('addToFavorite/<int:pk>', views.addToFavorite, name='addFavorite'),
	path('accounts/', include('allauth.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)