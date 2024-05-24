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

