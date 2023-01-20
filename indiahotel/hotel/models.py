from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dishes(models.Model):
    name=models.CharField(max_length=100)
    category=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to="dish_imges",null=True)
    def __str__(self):
        return self.name
     