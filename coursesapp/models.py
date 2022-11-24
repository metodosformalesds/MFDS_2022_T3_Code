from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Perfil(models.Model):
    """
    Por Cinthia Elena Hernández Rodríguez
    Se crea una clase con el nombre de Perfil, esta clase servirá para crear la tabla de base de datos "Perfil" con los campos de "user, skills, pais y avatar". Se debe tomar en cuenta que al querer
    lograr que cada usuario tenga su Perfil, entonces se crea una relación 1-1 con el modelo de Usuario por medio del campo "user". De esa forma se logra que cada usuario, tenga su Perfil único.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='profile_images', null=True, default='profile_images/default.png')

    # Python 3
    def __str__(self): 
        return self.user.username

#Modelo anterior, el nuevo es Curso

class Courses(models.Model):
    """
    Por Gerardo Andrés Félix Irigoyen
    Se crea una clase con el nombre de Courses, esta clase servirá para crear la tabla de base de datos "Courses", la cual contiene todos los cursos 
    extraidos de Udemy. En primera instancia no se definieron llaves foraneas, por eso se descarto.
    """
    id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)
    price = models.FloatField(max_length=5)
    url = models.URLField(max_length=255)
    category = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    language = models.CharField(max_length=4)
    platform = models.CharField(max_length=20, null = True)
    instructor = models.CharField(max_length=100, null = True)
    level = models.CharField(max_length=20, null = True)


class Curso(models.Model):
    """
    Por Gerardo Andrés Félix Irigoyen
    Se crea una clase con el nombre de Curso, esta clase servirá para crear la tabla de base de datos "Courses", la cual contiene todos los cursos 
    extraidos de Udemy. A diferencia de la anterior se le declara llave foranea y campo de favoritos que es una relacion muchos a muchos. 
    """
    id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    url = models.URLField(max_length=255)
    category = models.TextField()
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    language = models.CharField(max_length=4)
    instructor = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    tags = models.TextField(null=True)
    platform = models.CharField(max_length=50, null=True)
    favorites = models.ManyToManyField(User, related_name='favorite')


    def __str__(self):
        return self.title


class Comment(models.Model):
    """
    Por Gerardo Andrés Félix Irigoyen
    Se crea una clase con el nombre de Comment, esta clase servirá para crear la tabla de base de datos "Comment", lla cual contiene los comentarios hechos por los 
    usuarios en la sección de cursos. Cuenta con dos llaves foraneas, la del usuario y la del curso.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField(max_length=500)

    def __str__(self):
        return self.user.username

    
class Job(models.Model):
    """
    Por Gerardo Andrés Félix Irigoyen
    Se crea una clase con el nombre de Job, esta clase servirá para crear la tabla de base de datos "Job", la cual contiene todos los puestos de trabajos
    extraidos de Indeed. 
    """
    id = models.CharField(primary_key=True, max_length=10)
    category = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    postDate = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.title

class Skills(models.Model):
    """
    Por Cinthia Elena Hernández Rodríguez
    Clase que contiene la estructura de la tabla Skills en la base de datos. Esta clase contiene 11 variables. Una hacia una relación 1-1 con el usuario del Modelo User y 10 restantes para almacenar
    las skills de los usuarios (5 soft skills y 5 hard skills)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    soft_skill1 = models.CharField(max_length=255, blank=True)
    soft_skill2 = models.CharField(max_length=255, blank=True)
    soft_skill3 = models.CharField(max_length=255, blank=True)
    soft_skill4 = models.CharField(max_length=255, blank=True)
    soft_skill5 = models.CharField(max_length=255, blank=True)
    hard_skill1 = models.CharField(max_length=255, blank=True)
    hard_skill2 = models.CharField(max_length=255, blank=True)
    hard_skill3 = models.CharField(max_length=255, blank=True)
    hard_skill4 = models.CharField(max_length=255, blank=True)
    hard_skill5 = models.CharField(max_length=255, blank=True)
    # Python 3
    def __str__(self): 
        return self.user.username

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    """
    Por Cinthia Elena Hernández Rodríguez
    Función que indica por medio del @receiver una señal. Una señal es una función que ejecuta una acción después de que sucede algo en la página. Para este caso
    la señal cumple con la función de crear un objeto de tipo Perfil para el usuario registrado en la página. Cada usuario que se regsitre, crea un objeto de tipo Perfil y se enlazan por la variable User.
    """
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)

        print("Se enlaza el objeto Skills y Perfil con el usuario")

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    """
    Por Cinthia Elena Hernández Rodríguez
    Función que indica por medio del @receiver una señal. Una señal es una función que ejecuta una acción después de que sucede algo en la página. Para este caso
    la señal cumple con la función de crear un objeto de tipo Skills para el usuario registrado en la página. Cada usuario que se registre, crea un objeto de tipo Skills y se enlazan por la variable User.
    """
    if kwargs.get('created', False):
        Skills.objects.get_or_create(user=instance)
        print("Se enlaza el objeto Skills de usuario")
