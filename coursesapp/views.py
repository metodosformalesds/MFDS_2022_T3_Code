"""
Las vistas nos permiten a nosotros definir la lógica que tendrá nuestra aplicación. Aquí también añadimos información lógica de los modelos.
"""
from django.shortcuts import render, redirect #Importamos funciones para renderizar páginas y también reedirigir usuarios
from django.http import HttpResponse


from django.contrib.auth import authenticate, login, logout #Importamos funciones para revisar el login de usuarios 

from django.contrib import messages #Importamos funciones para mostrar mensajes dependiendo de acciones

from django.contrib.auth.decorators import login_required #Importamos una función que nos permite revisar si el usuario está con sesión activa

from .forms import CreateUserForm # Importamos del archivo forms.py la función que nos permite importar formularios

from .models import Courses, Curso # Importamos los modelos que creamos en models.py, Courses es el modelo anterior

from django.views.decorators.csrf import csrf_exempt  #

from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance, SearchVector

from .forms import  UpdateUserFormAvatar, UpdateUserFormEmail, SetPasswordForm

from .forms import UpdateProfileForm

from .forms import UpdateUserForm

#@login_required(login_url='login') #@login_required nos indica que, lo que está dentro de login_required se ejecutará únicamente cuando el usuario está con sesión activa.
def home(request): #Definimos el nombre de la función home que será nuestra vista principal
	"""
 Función home

	Args:
		request ()

	Returns:
		render: Renderiza lo que tenga el documento html dashboard.html
	"""

	courses = Curso.objects.all()[:5] #Obtenemos 10 cursos de la base de datos 

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
	if request.user.is_authenticated: #Si el usuario esta loggeado

		courses = Curso.objects.all()[:3]
		courses1 = Curso.objects.all()[4:7] 
		return render(request, 'profile.html', {'courses': courses,'courses1': courses1})
	else : 
		return redirect('home')

def profileConfig(request): 
	"""
	Función profileConfig: Lógica de la vista de la configuración del perfil del usuario

		Args:

		Returns:
			render: Renderización del archivo "profileConfig.html"
	"""
	if request.user.is_authenticated: #Si el usuario esta loggeado
		if request.method == 'POST': #si el método que se recibe es POST 
			user_form = UpdateUserForm(request.POST, instance=request.user)
			profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.perfil)

			if user_form.is_valid() and profile_form.is_valid(): #si son validos ambos formularios
				user_form.save()
				profile_form.save()
				return redirect('profile') #te manda al perfil 
				
		else:
			user_form = UpdateUserForm(instance=request.user)
			profile_form = UpdateProfileForm(instance=request.user.perfil)


		return render(request, 'profileConfig.html', {'user_form': user_form, 'profile_form': profile_form})
	else:
		return redirect('home')

def courses(request): 
	"""
	Función courses: Lógica de la vista de los cursos buscados y obtenidos por medio de la API

		Args:

		Returns:
			render: Renderización del archivo "courses.html"
			return: Retona los cursos buscados. 
	"""
	courses = Curso.objects.all()[::] 
	return render(request, 'courses.html', {'courses': courses})

def courses_for_category(request, category): 
	"""
	Función courses_for_category: Lógica de la vista de los cursos de cada categoría

		Args:
		category: Indica la categoria que se está buscando.

		Returns:
			render: Renderización del archivo "courses.html"
			return: retorna los cursos filtrados por categoría.
	"""
	courses = Curso.objects.all()[:3]
	#Depende de la categoría, realizamos la consulta a la base de datos
	if category == 'backend':
		courses = Curso.objects.filter(category='backend')
	elif category == 'frontend':
		courses = Curso.objects.filter(category='frontend')
	elif category == 'fullstack':
		courses = Curso.objects.filter(category='fullstack')
	elif category == 'datascience':
		courses = Curso.objects.filter(category='datascience')
	elif category == 'cybersecurity':
		courses = Curso.objects.filter(category='cybersecurity')

	return render(request, 'courses.html', {'courses': courses})


def courseView(request, id): 
	"""
	Función courseView: Lógica de la vista individual de los cursos

		Args:

		Returns:
			render: Renderización del archivo "courseView.html"
	"""
	course = Curso.objects.get(id=id)
	return render(request, 'courseView.html', {'course': course})

def jobs(request): 
	"""
	Función jobs: Lógica de la vista de los trabajos buscados por el usuario. 

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
	"""
	Función searchBar: Muestra la lógica para la búsqueda de cursos

		Args:

		Returns:
			render: Renderización del archivo "courses.html"
	"""

	if request.method == 'POST':
		search = request.POST.get('search', '')
		
		courses = (Curso.objects.annotate(similarity=TrigramSimilarity('description', search)).filter(similarity__gte=0.1).order_by('-similarity'))

		#save queries by user in the database
		'''
		query = Query()
		query.user = request.user
		query.query = search
		query.save()
		'''
		return render(request, 'courses.html', {'courses': courses})
	else:
		return render(request, 'courses.html')

def profileConfigAvatar(request):

	if request.user.is_authenticated:
		if request.method == 'POST': 
			profile_form = UpdateUserFormAvatar(request.POST, request.FILES, instance=request.user.perfil)

			if profile_form.is_valid():
				profile_form.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			profile_form = UpdateUserFormAvatar(instance=request.user.perfil)

		return render(request, 'profileConfigAvatar.html', {'profile_form': profile_form})
	else:
		return redirect('home')

def profileConfigEmail(request):

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			user_form = UpdateUserFormEmail(request.POST, instance=request.user)
			if user_form.is_valid():
				user_form.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			user_form = UpdateUserFormEmail(instance=request.user)

		return render(request, 'profileConfigEmail.html', {'user_form': user_form})
	else:
		return redirect('home')

def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'profileConfigPassword.html', {'form': form})