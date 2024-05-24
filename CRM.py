# ALL GLORY TO MY LORD AND SAVIOR JESUS CHRIST FOR ALL HE HAS DONE!
# ALL GLORY TO JESUS CHRIST WHO IS THE ONLY ALMIGHTY GOD! FOR ALL Success HE GIFTS ME WITH

# Tomorrow we will memeorize and write out home_view, create_account_view, account_view, search_bar_view, opportunity models

# CRM models 
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Clear and Intuitive Navigation

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

# in this model we are going to offer a coupon for 40% off their first purchase if the user gives us their email so we can have them in our
# ecosystem and upsell them in the future 

def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))

        cart, created = get_or_create_cart(user=user, customer_id=customer_id)

        product = get_object_or_404(Product, pk=product_id)

        cart.products.add(product, through_defaults={'quantity': quantity})
        
        message = 'Your Product has successfully been added to cart'
        return redirect('cart_detail', message)
    
def remove_from_cart(request):
    if request.method == 'POST':
        user = request.user
        customer_id = request.POST.get('customer_id')
        product_id = request.POST.get('product_id')

        cart, created = get_or_create_cart(user=user, customer_id=customer_id)

        product = get_object_or_404(Product, pk=product_id)

        cart_item = get_object_or_404(CartItem, cart=cart, product=product)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        message = 'The Product has been successfully removed from cart'
        return redirect('cart_detail', message)
    
def cart_view(request):
    cart = Cart.objects.filter(user=request.user).first()
    if cart:
        cart_items = CartItem.objects.filter(cart=cart)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(request, 'cart_detail.html', {'cart_items': cart_items})
    else:
        return render(request, 'empty_cart.hmtl')
    
def cart_checkout_view(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    cart_items = CartItem.objects.filter(cart=cart)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    context={
        'cart_items': cart_items
        'total_price': total_price
    }
    return render(request, 'cart_detail.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('home'))
        else:
            error_message = 'Invalid username or password'
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')

@login_required
def contact_us(request):
    if request.method =='POST':
        user = request.user
        customer_id = request.POST.get('customer_id')
        message = request.POST.get('message')

        message_to_user = 'Your message has been received! Thank You for your time!'

        return render(request, 'home.html', {'message': message_to_user})
    else:
        return render(request, 'contact_us.hmtl')


def home_view(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'home.html', context)

def create_account_view(request):
    form = CreateAccountForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('account_view')
    
    context = {
        'form': form,
        'title': 'Create Account'
    }
    return render(request, 'create_account.html', context)

@login_required
def account_view(request):
    account = Account.objects.filter(user=request.user).first()
    context = {
        'account': account,
        'title': 'Account'
    }
    return render(request, 'account_view.html', context)


















































































































































def home_view(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'home.html', context)



def create_account_view(request):
    form = CreateAccountForm(request.POST or None):
    if form.is_valid():
        form.save()
        return redirect('account_view')
    
    context = {
        'form': form,
        'title': 'Create Account'
    }
    return render(request, 'create_account.html', context)

































































































































































