from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    web = models.URLField(blank=True)

    # Python 3
    def __str__(self): 
        return self.usuario.username

class Courses(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=1)
    url = models.URLField(max_length=255)
    category = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=5, decimal_places=1)
    language = models.CharField(max_length=4)
    platform = models.CharField(max_length=20, null = True)
    instructor = models.CharField(max_length=50, null = True)


    def __str__(self):
        return self.title
    
