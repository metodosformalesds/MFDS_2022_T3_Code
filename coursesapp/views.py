"""
Las vistas nos permiten a nosotros definir la lógica que tendrá nuestra aplicación. Aquí también añadimos información lógica de los modelos.
"""
from django.shortcuts import render, redirect, get_object_or_404 #Importamos funciones para renderizar páginas y también reedirigir usuarios
from django.http import HttpResponse, HttpResponseRedirect


from django.contrib.auth import authenticate, login, logout #Importamos funciones para revisar el login de usuarios 
from django.contrib import messages #Importamos funciones para mostrar mensajes dependiendo de acciones
from django.contrib.auth.decorators import login_required #Importamos una función que nos permite revisar si el usuario está con sesión activa
from .forms import CreateUserForm # Importamos del archivo forms.py la función que nos permite importar formularios
from .models import Curso # Importamos los modelos que creamos en models.py, Courses es el modelo anterior
from .models import Job, Skills, Comment
from django.views.decorators.csrf import csrf_exempt  #
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance, SearchVector, SearchQuery, SearchRank
from .forms import  UpdateUserFormAvatar, UpdateUserFormEmail, SetPasswordForm, SoftSkill1_form, SoftSkill2_form
from .forms import UpdateProfileForm
from .forms import UpdateUserForm, SoftSkill3_form, SoftSkill4_form, SoftSkill5_form
from .forms import HardSkill1_form,HardSkill2_form,HardSkill3_form,HardSkill4_form,HardSkill5_form, addCommentForm
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
	jobs = Job.objects.all()[:5]

	return render(request, 'dashboard.html', {'courses': courses, 'jobs': jobs}) #Renderizamos el contenido dentro de dashboard.html y le pasamos un diccionario con la consulta

@csrf_exempt
def registerPage(request): # Se define el nombre de la función registerPage
	"""
	Por Cinthia Elena Hernández Rodríguez

	Función registerPage: Reedirecciona en caso de que el usuario este autenticado (loggeado) la página "home", esto para evitar que un usuario loggeado acceda. En caso de no estar loggeado
	se obtiene el formulario "CreateUserForm" y se guarda en "form". Esta variable esperará una solicitud de tipo POST, si es de tipo POST se obtienen los datos y en caso de ser válido se guardan los datos
	del formlario, además de ello, se recibe el username y el password para autenticar al usuario (iniciar sesión) y llevarlo al "home".
	Todo esto sucede en el render que contiene el documento html register.html

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
	Por Cinthia Elena Rodriguez Hernandez

	Función loginPage: Tiene como finalidad ser la vista de login, esta función recibe una solicitud de acceso cuando el usuario entra en el link y en caso de que ya se encuentre loggeado el usuario
	entonces lo reedirigirá al "home", en caso de no estarlo, se obtiene de un formulario con solicitud de tipo POST (de envío de datos). Se obtiene el usuario y la contraseña de ese formulario y se autentica
	al usuario por medio de la función "authenticate" que se almacena en la variable user. Se hace el login y en caso de hacerlo correctamente, se manda al "home". En caso contrario, se manda un mensaje de error.
	Todo esto sucede en el render que contiene el documento html login.html

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
	Por Cinthia Elena Hernández Rodríguez 

	Función logoutUser: Su funcionalidad es cerrar sesión al usuario cuando este haga click en cerrar sesión.
	Recibe una solicitud y se reedirecciona al login una vez que cerró sesión.

	Args:
		request ():

	Returns:
		redirect: Reedirige al login al usuario después de cerrar sesión con la función logout
	"""
	logout(request)
	return redirect('login')

def profileUser(request): 
	"""
	Por Cinthia Elena Hernández Rodríguez

	Función profileUser: Esta función tiene la funcionalidad de dar lógica a la vista que renderiza el perfil del usuario en el documento html "profile.html". La forma en la que lo hace es primero condicionando
	su vista a que el usuario tenga sesión activa. Si no, el usuario es llevado al "home". Si tiene sesión iniciada, se guardan en unas variables algunos objetos de tipo curso que son mostrados al usuario
	en su perfil.

		Args:
			request ():
		Returns:
			render: Renderización del archivo "profile.html"
			redirect: si el usuario no esta autenticado lo reedirige a "home", la vista principal. 
	"""

	if request.user.is_authenticated: #Si el usuario esta loggeado

		courses = Curso.objects.all()[:3]
		courses1 = Curso.objects.all()[4:7] 
		return render(request, 'profile.html', {'courses': courses,'courses1': courses1})
	else : 
		return redirect('home')

@csrf_exempt
def profileConfig(request): 
	"""
	Por Cinthia Elena Hernández Rodríguez

	Función profileConfig: Esta función sirve para brindar de lógica a la vista del documeto html "profileConfig.html". Primero condiciona su renderizado a si el usuario está loggeado, si no está loggeado, entonces
	es llevado el "home". Si está loggeado, entonces se espera una solicitud de tipo POST en un formulario que servirá para editar los parámetros de "Nombre, Apellido y País" declarados en el modelo de Perfil y User.
	Dichos formularios "UpdateUserForm" y "UpdateProfileForm" creados con anterioridad en forms.py esperan las variables antes mencionadas. Si ambos formularios son llenados correctamente (no basta uno), entonces
	se guardan los datos. En caso contrario, se recarga la página y no realiza ninguna acción hasta que este llenado correctamente.
	Función profileConfig: Lógica de la vista de la configuración del perfil del usuario

		Args:
			request ():
		Returns:
			render: Renderización del archivo "profileConfig.html"
			redirect: si el usuario no esta autenticado lo reedirige a "home", la vista principal. 
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
	return render(request, 'courseView.html', {'course': course} )


def jobs_for_title(request, title): 
	"""
	Función jobs_for_title: Lógica de la vista de los trabajos de cada title
		Args:
		title: Indica el title que se está buscando.
		Returns:
			render: Renderización del archivo "jobs.html"
			return: retorna los trabajos filtrados por title.
	"""
	jobs = title.objects.all()[:3]
	#Depende de la categoría, realizamos la consulta a la base de datos
	#Cambiar Title por Job
	if title == 'backend':
		jobs = title.objects.filter(title='backend')
	elif title == 'frontend':
		jobs = title.objects.filter(title='frontend')
	elif title == 'fullstack':
		jobs = title.objects.filter(title='fullstack')
	elif title == 'datascience':
		jobs = title.objects.filter(title='datascience')
	elif title == 'cybersecurity':
		jobs = title.objects.filter(title='cybersecurity')

	return render(request, 'jobs.html', {'jobs': jobs})


def jobs(request): 
	"""
	Función jobs: Lógica de la vista de los trabajos buscados por el usuario. 

		Args:

		Returns:
			render: Renderización del archivo "jobs.html"
	"""
	jobs = Job.objects.all()[::]
	result = jobs.order_by('postDate')

	return render(request, 'jobs.html', {'jobs': result})

@csrf_exempt
def skills(request): 
	"""
	 Por Cinthia Elena Hernández Rodríguez
	 Función skills: Muestra la lógica para la edición de skills

		Args:
			request()
		Returns:
			render: Renderización del archivo html "skills.html"
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

		courses = Curso.objects.annotate(similarity=TrigramSimilarity('url', search),).filter(similarity__gte=0.1).order_by('-similarity')

		if courses:
			return render(request, 'courses.html', {'courses': courses})
		else:
			courses = Curso.objects.annotate(search=SearchVector('title', 'description', 'url')).filter(search=search) 
			return render(request, 'courses.html', {'courses': courses})

		#save queries by user in the database
	else:
		return render(request, 'courses.html')


@csrf_exempt
def searchBarJob(request): 
	"""
	Función searchBar: Muestra la lógica para la búsqueda de trabajos

		Args:

		Returns:
			render: Renderización del archivo "jobs.html"
	"""

	if request.method == 'POST':
		search = request.POST.get('search', '')

		jobs = Job.objects.annotate(similarity=TrigramSimilarity('url', search),).filter(similarity__gte=0.1).order_by('-similarity')

		if jobs:
			return render(request, 'jobs.html', {'jobs': jobs})
		else:
			jobs = Job.objects.annotate(search=SearchVector('title', 'description', 'url')).filter(search=search) 
			return render(request, 'jobs.html', {'jobs': jobs})

		#save queries by user in the database
	else:
		return render(request, 'jobs.html')

@csrf_exempt
def profileConfigAvatar(request):
	"""
	  Por Cinthia Elena Hernández Rodríguez
		
		Función profileConfigAvatar: Renderizará el formulario de editar imagen de perfil. Para hacerlo correctamente, condiciona que el usuario este loggeado. Si lo está espera de un formulario tipo POST que
		los datos que recibe de él coincidan con el formulario "UpdateUserFormAvatar", en este caso, un archivo de imagen. Si es así, lo guarda. Todo esto ocurre en la rendeización del documento html "profileConfigAvatar.html"
		
		Args:
			request()
		Returns:
			render: Renderización del archivo html "profileConfigAvatar.html"
			redirect: Si el formulario es validado correctamente se redirige al profile y se muestran los cambios
			redirect: Si el usuario no esta autenticado se redirige al home
	"""

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

@csrf_exempt
def profileConfigEmail(request):
	"""
  	Por  Cinthia Elena Hernández Rodríguez

	Función profileConfigEmail: Esta función permite dotar de lógica el formulario para editar el correo electrónico de un usuario. Esto lo hace, al igual que las demás funciones, que el usuario esté loggeado.
	Si lo está entonces recibe de un formulario tipo POST los datos (correo), si es válido lo guarda. Esto se hace en la renderización del documento html profileConfigEmail.

	Args:
		request()
	Returns:
		render: Renderización del archivo html "profileConfigEmail.html"
		redirect: Si el formulario es validado correctamente se redirige al profile y se muestran los cambios
		redirect: Si el usuario no esta autenticado se redirige al home

	"""

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

@csrf_exempt
def password_change(request):
	
	"""
	Por Cinthia Elena Hernández Rodríguez

	Función password_change: Para reaizar la funcionalidad de cambio de contraseña, se hizo uso del formulario SetPasswordForm, este formulario no fue diseñado por nosotros pues forma parte de los formularios
	predeterminados de Django, esto porque las contraseñas deben ser cifradas y no únicamente pasadas en texto plano. Al igual que las funciones anteriores, se espera que el usuario este loggeado. Si lo está
	entonces al igual que en los demás, se espera el formulario sea válido y entonces es guardado. Esto se hace renderizando "profileConfigPassword.html"
	
	Args:
		request()
	Returns:
		render: Renderización del archivo html "profileConfigPassword.html"
		redirect: Si el formulario es validado correctamente se redirige al profile y se muestran los cambios
		redirect: Si el usuario no esta autenticado se redirige al home

 	"""
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

@login_required
def favorite_add(request, id):
	"""
	Función favorite_add: Muestra la lógica para la búsqueda de cursos

		Args:

	Returns:
			HttpResponseRedirect: Redireccion a la pagina actual
	"""
	"""
	Función favorite_add: Muestra la lógica para la búsqueda de cursos

		Args:

	Returns:
			HttpResponseRedirect: Redireccion a la pagina actual
	"""
	course = get_object_or_404(Curso, id=id)
	if course.favorites.filter(id=request.user.id).exists():
		course.favorites.remove()
	else:
		course.favorites.add()
	return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def favorite_list(request):
	"""
	Función searchBar: Muestra la lógica para la búsqueda de trabajos

		Args:

		Returns:
			render: Renderización del archivo "favorite.html"
	"""	
	new = Curso.objects.filter(favorites=request.user)
	return render(request, 'favorite.html', {'new':new})


"""_summary_
	Por Cinthia Elena Hernández Rodríguez
	
	Estas funciones sirven de lógica a los templates
	de edición de skills (5 hard skills y 5 soft skills). Las siguientes 10 plantillas funcionan de la misma manera, variando únicamente en el dato que guardan en la base de datos por lo que su documentación
	individual parece redundante. La funcionalidad general es revisar si el usuario esta loggeado. Si lo está, entonces esperará que el usuario mande un formulario de tipo POST que se renderiza del documento
	html. Una vez llenado, se valida la información y se guarda.

"""


@login_required
def favorite_list(request):
	"""
	Función searchBar: Muestra la lógica para la búsqueda de trabajos

		Args:

		Returns:
			render: Renderización del archivo "favorite.html"
	"""	
	new = Curso.objects.filter(favorites=request.user)
	return render(request, 'favorite.html', {'new':new})

@csrf_exempt
def SoftSkill1(request):
	"""
	Por Cinthia Elena Hernández Rodríguez

	Esta función sirve de lógica al formulario que se renderiza del archivo html correspondiente. Al igual que los antecesores, recibe una solicitud de tipo POST en un formulario. Una vez recogida la solicitud,
	se valida la información y se guarda en la base de datos. Una vez guardado correctamente, el usuario es llevado el "profile". Todo esto, esperando el usuario este loggeado, sino, es llevado automatizamente al
	"home"

	Args:
		request()
	Returns:
		render: Renderización del archivo html de la skill correspondiente.
		redirect: Si el formulario es validado correctamente se redirige al profile y se muestran los cambios
		redirect: Si el usuario no esta autenticado se redirige al home

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = SoftSkill1_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = SoftSkill1_form(instance=request.user.skills)

		return render(request, 'softskill1.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')




@csrf_exempt
def SoftSkill2(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = SoftSkill2_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = SoftSkill2_form(instance=request.user.skills)

		return render(request, 'softskill2.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')


@csrf_exempt
def SoftSkill3(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = SoftSkill3_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = SoftSkill3_form(instance=request.user.skills)

		return render(request, 'softskill3.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')

@csrf_exempt
def SoftSkill4(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = SoftSkill4_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = SoftSkill4_form(instance=request.user.skills)

		return render(request, 'softskill4.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')

@csrf_exempt
def SoftSkill5(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = SoftSkill5_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = SoftSkill5_form(instance=request.user.skills)

		return render(request, 'softskill5.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')


@csrf_exempt
def HardSkill1(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = HardSkill1_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = HardSkill1_form(instance=request.user.skills)

		return render(request, 'hardskill1.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')

@csrf_exempt
def HardSkill2(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = HardSkill2_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = HardSkill2_form(instance=request.user.skills)

		return render(request, 'hardskill2.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')

@csrf_exempt
def HardSkill3(request):
	
	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = HardSkill3_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = HardSkill3_form(instance=request.user.skills)

		return render(request, 'hardskill3.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')

@csrf_exempt
def HardSkill4(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = HardSkill4_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = HardSkill4_form(instance=request.user.skills)

		return render(request, 'hardskill4.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')

@csrf_exempt
def HardSkill5(request):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""

	if request.user.is_authenticated: 
		if request.method == 'POST': 
			skills_forms = HardSkill5_form(request.POST, instance=request.user.skills)
			if skills_forms.is_valid():
				skills_forms.save()
				messages.success(request, 'Your profile is updated successfully')
				return redirect('profile')
				#return render(request,'profile.html')
		else:
			skills_forms = HardSkill5_form(instance=request.user.skills)

		return render(request, 'hardskill5.html', {'skills_forms': skills_forms})
	else:
		return redirect('home')


@csrf_exempt
def addComment(request, id):

	"""
	Por Cinthia Elena Hernández Rodríguez

	"""
	
	comment=Comment()
	if request.user.is_authenticated: 
		course = get_object_or_404(Curso, id=id)
		if request.method == 'POST':
			commentForm = addCommentForm(request.POST, instance=comment)
			comment.course = course
			comment.user = request.user
			if commentForm.is_valid():
				#comment.save()
				commentForm.save()

		messages.success(request, 'Your comment was created')
		#return redirect('courseView/'+str(id)
		return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



