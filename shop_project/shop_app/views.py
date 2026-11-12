from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FilterForm, OrderForm, ReviewForm
from .models import AnimalType, Order, OrderItem, OrderStatus, Product


def catalog(request):
    form = FilterForm(request.GET)
    products = Product.objects.annotate(rating=Avg('reviews__rating'))
    current_type = None

    if form.is_valid():
        data = form.cleaned_data
        current_type = data['type']
        if data['q']:
            products = products.filter(name__icontains=data['q'])
        if data['type']:
            products = products.filter(subtypes__animal_type=data['type'])
        if data['category']:
            products = products.filter(category__in=data['category'])
        if data['age']:
            products = products.filter(age__in=data['age'])
        if data['size']:
            products = products.filter(size__in=data['size'])
        if data['manufacturer']:
            products = products.filter(manufacturer__in=data['manufacturer'])
        if data['price_min'] is not None:
            products = products.filter(price__gte=data['price_min'])
        if data['price_max'] is not None:
            products = products.filter(price__lte=data['price_max'])
        if data['rating']:
            products = products.filter(rating__gte=int(data['rating']))
        products = products.distinct()

    return render(request, 'catalog.html', {
        'form': form,
        'products': products,
        'types': AnimalType.objects.all(),
        'current_type': current_type,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    rating = reviews.aggregate(Avg('rating'))['rating__avg']
    form = ReviewForm()

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product', pk=pk)

    return render(request, 'product.html', {
        'product': product,
        'reviews': reviews,
        'rating': rating,
        'form': form,
    })


def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect('catalog')
    return render(request, 'login.html', {'form': form})


def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('catalog')
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('catalog')


def cart(request):
    cart_data = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, quantity in cart_data.items():
        product = Product.objects.filter(pk=product_id).first()
        if product:
            items.append({'product': product, 'quantity': quantity, 'sum': product.price * quantity})
            total += product.price * quantity
    return render(request, 'cart.html', {'items': items, 'total': total})


def cart_add(request, pk):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        cart_data = request.session.get('cart', {})
        count = cart_data.get(str(pk), 0)
        if count < product.quantity:
            cart_data[str(pk)] = count + 1
            request.session['cart'] = cart_data
    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


def cart_remove(request, pk):
    if request.method == 'POST':
        cart_data = request.session.get('cart', {})
        cart_data.pop(str(pk), None)
        request.session['cart'] = cart_data
    return redirect('cart')


def order_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
    cart_data = request.session.get('cart', {})
    if not cart_data:
        return redirect('cart')

    form = OrderForm(request.POST or None)
    if form.is_valid():
        status, created = OrderStatus.objects.get_or_create(name='Создан')
        order = Order.objects.create(
            user=request.user,
            pickup_point=form.cleaned_data['pickup_point'],
            payment_method=form.cleaned_data['payment_method'],
            status=status,
        )
        for product_id, quantity in cart_data.items():
            product = Product.objects.filter(pk=product_id).first()
            if product:
                OrderItem.objects.create(
                    order=order, product=product, quantity=quantity, price=product.price
                )
                product.quantity = max(product.quantity - quantity, 0)
                product.save()
        request.session['cart'] = {}
        return redirect('orders')

    return render(request, 'order_form.html', {'form': form})


def orders(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user_orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'orders.html', {'orders': user_orders})