from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import  ContactForm, ReviewForm, CustomUserCreationForm
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.contrib.auth.hashers import make_password

#The views logic
def customer_registration_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Hash the password using make_password
            password = make_password(form.cleaned_data['password'])
            
            # Create a new user instance with the hashed password
            user = User.objects.create(username=form.cleaned_data['username'],email =form.cleaned_data['email'], password=password)
            
            # Optionally, you can set additional user attributes
            #user.first_name = form.cleaned_data['first_name']
            #user.last_name = form.cleaned_data['last_name']
            
            # Save the user
            user.save()
            
            messages.success(request, 'You have successfully registered. Please log in.')
            return redirect('login')  # Redirect to login page after successful registration
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration.html', {'form': form})


def customer_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/login_success_view/')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

@login_required
def customer_logout_view(request):
    logout(request)
    return redirect('home')

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Perform any other actions, such as sending emails
            return redirect('contact_success')  # Redirect to a success page after successful form submission
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'contact_success.html')

def login_success_view(request):
    return render(request, 'login_success.html')

def store(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store.html', context)


def product_detail(request, vehicle_id):
    product = Product.objects.get(pk=vehicle_id)
    albums = product.productalbum_set.all()
	
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Assuming you have implemented user authentication
            review.product = product
            review = Review.objects.create(customer=review.user, product=review.product, rating=form.cleaned_data['rating'], review_text=form.cleaned_data['review_text'])
            review.save()
            return redirect('vehicle_detail', vehicle_id=vehicle_id)
    else:
        form = ReviewForm()
    return render(request, 'product_detail.html', {'product': product, 'form': form, 'albums':albums})
@login_required(login_url='/customer_registration_view/')
def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'cart.html', context)
@login_required(login_url='/customer_login_view/')
def checkout(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'checkout.html', context)
@login_required(login_url='/customer_login_view/')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()
	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)
@login_required(login_url='/customer_login_view/')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)
	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if total == order.get_cart_total:
		order.complete = True
	order.save()
	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)
	return JsonResponse('Payment submitted..', safe=False)

def lexus(request):
	lexus = Product.objects.filter(make='Lexus')
	context = {
		'lexus':lexus,
	}
	return render(request, 'lexus.html', context)
def bmw(request):
	bmws = Product.objects.filter(make='BMW')
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	bmws = Product.objects.filter(make='BMW')
	context = {'bmws':bmws, 'cartItems':cartItems}
	return render(request, 'bmw.html', context)
def mercedes(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	mercs = Product.objects.filter(make='Mercedes')
	context = {'mercs':mercs, 'cartItems':cartItems}
	return render(request, 'mercedes.html', context)



def mazda(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	mazdas = Product.objects.filter(make='Mazda')
	context = {'mazdas':mazdas, 'cartItems':cartItems}
	return render(request, 'mazda.html', context)



def audi(request):
	data = cartData(request)
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	audis = Product.objects.filter(make='Audi')
	context = {'audis':audis, 'cartItems':cartItems}
	return render(request, 'audi.html', context)




def product_search(request):
    products = Product.objects.all()
    

    if request.method == 'POST':
        make = request.POST['make']
        min_price = request.POST['min_price']
        max_price = request.POST['max_price']
        min_mileage = request.POST['min_mileage']
        max_mileage = request.POST['max_mileage'] 
      
        if make:
            products = products.filter(make__icontains=make)
        if min_price is not None and max_price is not None:
            products = products.filter(price__range=(min_price, max_price))
        if min_mileage is not None and max_mileage is not None:
              products = products.filter(mileage__range=(min_mileage, max_mileage))

    return render(request, 'search_results.html', {'products': products}) 




