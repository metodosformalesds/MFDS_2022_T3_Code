"""
Las vistas nos permiten a nosotros definir la lógica que tendrá nuestra aplicación. Aquí también añadimos información lógica de los modelos.
"""
from django.shortcuts import render, redirect #Importamos funciones para renderizar páginas y también reedirigir usuarios
from django.http import HttpResponse


from django.contrib.auth import authenticate, login, logout #Importamos funciones para revisar el login de usuarios 

from django.contrib import messages #Importamos funciones para mostrar mensajes dependiendo de acciones

from django.contrib.auth.decorators import login_required #Importamos una función que nos permite revisar si el usuario está con sesión activa

from .forms import CreateUserForm # Importamos del archivo forms.py la función que nos permite importar formularios

#@login_required(login_url='login') #@login_required nos indica que, lo que está dentro de login_required se ejecutará únicamente cuando el usuario está con sesión activa.
def home(request): #Definimos el nombre de la función home que será nuestra vista principal
	"""
 Función home

	Args:
		request ()

	Returns:
		render: Renderiza lo que tenga el documento html dashboard.html
	"""

	return render(request, 'dashboard.html') #Renderizamos el contenido dentro de dashboard.html 

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