from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

   
class User(AbstractUser):
    id = models.AutoField(primary_key=True, editable=False)
    username = models.CharField(max_length=100 ,unique=True)
    email = models.EmailField(unique=True)
    

    def __str__(self):
        return self.username


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name