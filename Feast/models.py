from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Menu(models.Model):
    fooditem=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField(upload_to= 'images')
    def __str__(self):
        return self.fooditem


class CustomUser(AbstractUser):
     def __str__(self):
        return self.username
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Reference the custom user model
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return f'{self.user.username} - {self.menu.fooditem}'

