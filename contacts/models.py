from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
# Create your models here.




class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    dob = models.DateField()
    mobile = models.CharField(max_length=30)


class Account(models.Model):
  account_number = models.CharField(max_length=30)
  account_type = models.CharField(max_length=20)
  open_date = models.DateField()
  balance = models.DecimalField(default=0, decimal_places=2, max_digits=12)
  user = models.ForeignKey(User, related_name='accounts', on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=20)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=8)


class Order(models.Model):
    order_date = models.DateField()
    status = models.CharField(max_length=20)
    products = models.ManyToManyField(Product, through='Detail')


class Detail(models.Model):
    product     = models.ForeignKey(Product, on_delete=models.CASCADE)
    order       = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity    = models.IntegerField(default=1)