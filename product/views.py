from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms


# Create your models here.

class Category(models.TextChoices):
    SHIRTS = 'T-SHIRTS'
    PANTS = 'PANTS'
    CAPS = 'CAPS'

class Size(models.TextChoices):
    SMALL = 'SMALL'
    MEDIUM = 'MEDIUM'
    LARGE = 'LARGE'

class Status(models.TextChoices):
    pending = 'pending'
    Out_for_delivary = 'Out for delivary'
    deliverd = 'deliverd'

class Product(models.Model):
    name = models.CharField(max_length=200,default="",blank=False)
    main_image = models.ImageField(upload_to='photos/',default=timezone.now)
    firist_image = models.ImageField(upload_to='photos/',default=timezone.now)
    second_image = models.ImageField(upload_to='photos/',default=timezone.now)
    description = models.TextField(max_length=1000,default="",blank=False)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    brand = models.CharField(max_length=200,default="",blank=False)
    category = models.CharField(max_length=40,choices=Category.choices)
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    stocks = models.IntegerField(default=0)
    creatAt = models.DateField(auto_now=True)
    size = models.CharField(max_length=40,choices=Size.choices)
    user  = models.ForeignKey(User, null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, default='none')
    color = models.CharField(default='none', max_length=50)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    status = models.CharField(max_length=20, default='Pending')  # حالة الطلب، مثل "معلق"، "مؤكد"
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='photos/',default=timezone.now)
    size = models.CharField(max_length=40,default="none")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    color = models.CharField(default="none",max_length=50)
    status = models.CharField(max_length=20,choices=Status.choices, default='Pending')  # حالة الطلب، مثل "معلق"، "مؤكد

    first_name = models.CharField(max_length=100,default="none")
    last_name = models.CharField(max_length=100,default="none")
    company_name = models.CharField(max_length=100,default="none")
    address = models.CharField(max_length=250,default="none")
    email = models.EmailField(default="none")
    phone = models.CharField(max_length=15,default="none")
    additional_info = models.CharField(max_length=500,default="none")

    def __str__(self):
        return f'{self.product_name} - {self.user.username}'








