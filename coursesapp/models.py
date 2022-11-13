from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=255, blank=True)
    web = models.URLField(blank=True)

    # Python 3
    def __str__(self): 
        return self.usuario.username

class Course(models.Model):
    id = models.CharField(primary_key=True, max_length=10)
    title = models.CharField(max_length=100)
    price = models.FloatField(max_length=10)
    url = models.URLField(max_length=255)
    category = models.CharField(max_length=50)
    rating = models.FloatField(max_length=5)
    language = models.CharField(max_length=4)

    def __str__(self):
        return self.title
    
