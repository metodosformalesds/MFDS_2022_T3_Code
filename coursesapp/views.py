"""
Las vistas nos permiten a nosotros definir la lógica que tendrá nuestra aplicación. Aquí también añadimos información lógica de los modelos.
"""
from django.shortcuts import render, redirect #Importamos funciones para renderizar páginas y también reedirigir usuarios
from django.http import HttpResponse


from django.contrib.auth import authenticate, login, logout #Importamos funciones para revisar el login de usuarios 

from django.contrib import messages #Importamos funciones para mostrar mensajes dependiendo de acciones

from django.contrib.auth.decorators import login_required #Importamos una función que nos permite revisar si el usuario está con sesión activa

from .forms import CreateUserForm # Importamos del archivo forms.py la función que nos permite importar formularios

from .models import Courses # Importamos los modelos que creamos en models.py

from django.views.decorators.csrf import csrf_exempt  #

from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance, SearchVector


#@login_required(login_url='login') #@login_required nos indica que, lo que está dentro de login_required se ejecutará únicamente cuando el usuario está con sesión activa.
def home(request): #Definimos el nombre de la función home que será nuestra vista principal
	"""
 Función home

	Args:
		request ()

	Returns:
		render: Renderiza lo que tenga el documento html dashboard.html
	"""

	courses = Courses.objects.all()[:5] #Obtenemos 10 cursos de la base de datos 

	return render(request, 'dashboard.html', {'courses': courses}) #Renderizamos el contenido dentro de dashboard.html y le pasamos un diccionario con la consulta

@csrf_exempt
def registerPage(request): # Se define el nombre de la función registerPage
	"""
	Función registerPage: Vista de la página de registro

	Args:
		request ()

	Returns:
		render: Renderiza lo que tenga el documento html register.html en caso de que el usuario no tenga una sesión activa.
		render: Renderiza login en caso de que el formulario sea llenado correctamente
	"""

	if request.user.is_authenticated: # Si el usuario está con sesión activa, mandalo a home
		return redirect('home')
	else:
		form = CreateUserForm() # 
		if request.method == 'POST':
			form = CreateUserForm(request.POST) #Obten los datos del formulario creado
			if form.is_valid():
				form.save() #guarda los datos en la base de datos
				username = form.cleaned_data.get('username') #Obtenemos del formulario el nombre de usuario
				password = form.cleaned_data.get('password1') #Obtenemos del formulario la contraseña
				user = authenticate(request, username=username, password=password) #Autenticamos al usuario con los datos mencionados
				login(request, user) #iniciamos sesión con los datos de autenticación

				return redirect('home') #Si el formulario es correcto y guardo los datos, mandalo al home
			

		context = {'form':form}
		return render(request, 'register.html', context)

@csrf_exempt
def loginPage(request): #Se crea la funcion loginPage para crear la vista de login
	"""
 Función loginPage: Vista de la página de login

	Args:
		request ():

	Returns:
		render: Renderiza lo que tenga el documento html login.html en caso de que el usuario no tenga sesión activa
		render: Renderiza lo que tenga el documento html asociado a home en caso de que el formulario sea llenado correctamente y se haya autenticado el usuario
	"""
	if request.user.is_authenticated: # Si el usuario está con sesión activa, mandalo a home
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username') #Del formulario POST obtenemos el username y el password definidos en el login
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password) #Autenticamos al usuario con los datos mencionados

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Usuario o contraseña erroneos') #Si el usuario no ingresó datos correctos, entonces mandamos mensaje de error

		context = {}
		return render(request, 'login.html', context)

def logoutUser(request):
	"""
 Función logoutUser: Lógica al cerrar sesión activa

	Args:

	Returns:
		redirect: Reedirige al login al usuario después de cerrar sesión con la función logout
	"""
	logout(request)
	return redirect('login')

def profileUser(request): 
	"""
	Función profileUser: Lógica de la vista del perfil del usuario

		Args:

		Returns:
			render: Renderización del archivo "profile.html"
	"""
	courses = Courses.objects.all()[:3] #Obtenemos 10 cursos de la base de datos
	return render(request, 'profile.html', {'courses': courses})

def profileConfig(request): 
	"""
	Función profileUser: Lógica de la vista de la configuración del perfil del usuario

		Args:

		Returns:
			render: Renderización del archivo "profileConfig.html"
	"""
	return render(request, 'profileConfig.html')

def courses(request): 
	"""
	Función profileUser: Lógica de la vista de los cursos buscados y obtenidos por medio de la API

		Args:

		Returns:
			render: Renderización del archivo "courses.html"
	"""
	return render(request, 'courses.html')

def courses(request, category): 

	#Depende de la categoría, realizamos la consulta a la base de datos
	if category == 'backend':
		courses = Courses.objects.filter(category='backend')
	elif category == 'frontend':
		courses = Courses.objects.filter(category='frontend')
	elif category == 'fullstack':
		courses = Courses.objects.filter(category='fullstack')
	elif category == 'datascience':
		courses = Courses.objects.filter(category='datascience')
	elif category == 'cybersecurity':
		courses = Courses.objects.filter(category='cybersecurity')

	return render(request, 'courses.html', {'courses': courses})


def courseView(request): 
	"""
	Función courseView: Lógica de la vista individual de los cursos

		Args:

		Returns:
			render: Renderización del archivo "courseView.html"
	"""
	return render(request, 'courseView.html')

def jobs(request): 
	"""
	Función profileUser: Lógica de la vista de los trabajos buscados por el usuario. 

		Args:

		Returns:
			render: Renderización del archivo "jobs.html"
	"""
	return render(request, 'jobs.html')
def skills(request): 
	"""
	Función skills: Muestra la lógica para la edición de skills

		Args:

		Returns:
			render: Renderización del archivo "skills.html"
	"""
	return render(request, 'skills.html')


@csrf_exempt
def searchBar(request): 

	if request.method == 'POST':

		search = request.POST.get('search', '')
		#courses = Courses.objects.filter(url__icontains=search)
		#courses = Courses.objects.annotate(search=SearchVector('title', 'category'),).filter(search=search)  
		courses = (Courses.objects.annotate(similarity=TrigramSimilarity('url', search)).filter(similarity__gte=0.1).order_by('-similarity'))

		#print(Courses.objects.filter(title__trigram_similar=search))

		return render(request, 'courses.html', {'courses': courses})

	else:
		return render(request, 'courses.html')