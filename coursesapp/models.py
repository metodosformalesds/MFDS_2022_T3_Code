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
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=100)
    postDate = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    url = models.URLField(max_length=255)

    def __str__(self):
        return self.title
