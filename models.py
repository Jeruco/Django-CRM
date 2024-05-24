# ALL GLORY TO MY LORD AND SAVIOR JESUS CHRIST FOR ALL HE HAS DONE!
# ALL GLORY TO JESUS CHRIST WHO IS THE ONLY ALMIGHTY GOD! FOR ALL Success HE GIFTS ME WITH

# CRM models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()

class CreateAccount(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    status = models.CharFeield(max_length=50, choices=[('new', 'New'), ('qualified', 'Qualified'), ('contacted', 'Contacted'), ('won', 'Won'), ('lost', 'Lost')])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Deal(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    closed_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Account(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Cart(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    total_products = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(mx_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()

class AddToCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()

class RemoveFromCart(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()

class Login(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, unique=True)

class Logout(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

class ContactUs(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    your_message = models.CharField(max_length=1000)
    your_phone = models.CharField(max_length=20)

class SalesTripWire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    coupon = models.IntegerField()
