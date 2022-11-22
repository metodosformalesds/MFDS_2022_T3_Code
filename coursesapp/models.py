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


    def __str__(self):
        return self.title
    
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

@receiver(post_save, sender=User)
def create_profile(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)
        print("Se acaba de enlazar el usuario con su perfil")