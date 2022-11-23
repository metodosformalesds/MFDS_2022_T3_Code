from django.db import models
from django.contrib.auth.models import User


from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.CharField(max_length=255, blank=True)
    pais = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='profile_images', null=True, default='profile_images/default.png')

    # Python 3
    def __str__(self): 
        return self.user.username

#Modelo anterior, el nuevo es Curso
class Courses(models.Model):
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
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Curso, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return self.user.username

    
class Job(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    postDate = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.title

class Skills(models.Model):
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
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)
        print("Se acaba de enlazar el usuario con su perfil")