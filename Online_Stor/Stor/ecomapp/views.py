from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse  
from django.views.generic.list import ListView
from django.db.models import Q

from django.urls import reverse
from ecomapp.models import Category, Product, CartItem, Cart, Order
from ecomapp.forms import OrderForm, RegistrationForm, LoginForm
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib import auth
from decimal import Decimal




def base_view(request):
	try :
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except :
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	products = Product.objects.all()
	context = {
		'categories': categories,
		'products': products,
		'cart': cart
		
		
	}
	return render(request, 'base.html', context)

def product_view(request, product_slug):
	try :
		cart_id = request.session['cart_id']          #присваиваем cart_id значения данной сессии по ключу ['cart_id']
		cart = Cart.objects.get(id=cart_id)           #создаем корзину с нашим id который мы присвоили
		request.session['total'] = cart.items.count() # то количесво товара что есть в корзине 
	except :  #создаем коризну 
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	product = Product.objects.get(slug=product_slug)
	categories = Category.objects.all()
	context = {
		'product': product,
		'categories': categories,
		'cart': cart
		
	}
	return render(request, 'product.html', context)

def category_view(request, category_slug):
	try :
		cart_id = request.session['cart_id']          #присваиваем cart_id значения данной сессии по ключу ['cart_id']
		cart = Cart.objects.get(id=cart_id)           #создаем корзину с нашим id который мы присвоили
		request.session['total'] = cart.items.count() # то количесво товара что есть в корзине 
	except :  #создаем коризну 
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
	category = Category.objects.get(slug=category_slug)
	categories = Category.objects.all()
	products_of_category = Product.objects.filter(category=category) #отображает в category.html все продукты , что есть в ней 
	context = {
		'category': category,
		'products_of_category': products_of_category,
		'cart': cart,
		'categories': categories
	}
	return render(request, 'category.html', context)


def cart_view(request):
	try :
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except :
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context = {
	   'cart': cart,
	   'categories': categories
	}
	return render(request, 'cart.html', context)


def add_to_cart_view (request):
	try :
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except :
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)   
	product_slug = request.GET.get('product_slug')                                                                    #функция добовления товара в корзину
	product = Product.objects.get(slug=product_slug)
	cart.add_to_cart(product.slug)
	new_cart_total = 0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.catr_total = new_cart_total
	cart.save()
	return JsonResponse({
		'cart_total': cart.items.count(),
		'cart_total_price': cart.catr_total
		})


def remove_from_cart_view(request):
	try :
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except :
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)  #функция удаления товара в корзину
	product_slug = request.GET.get('product_slug') 
	product = Product.objects.get(slug=product_slug)
	cart.remove_from_cart(product.slug)
	new_cart_total = 0.00
	for item in cart.items.all():
		new_cart_total += float(item.item_total)
	cart.catr_total = new_cart_total
	cart.save()
	return JsonResponse({
		'cart_total': cart.items.count(),
		'cart_total_price': cart.catr_total
		})


def change_items_qty(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	qty = request.GET.get('qty')
	item_id = request.GET.get('item_id')
	cart.change_qty(qty, item_id)
	cart_item = CartItem.objects.get(id=int(item_id))
	return JsonResponse({
		'cart_total': cart.items.count(), 
		'item_total': cart_item.item_total,
		'cart_total_price': cart.catr_total
		})

def checkout_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	categories = Category.objects.all()
	context= {
			'cart': cart,
			'categories': categories
		}
	return render(request, 'checkout.html', context)


def order_create_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	context= {
			'form': form,
			'cart': cart,
			'categories': categories
	}
	return render(request, 'order.html', context)


def make_order_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = OrderForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		name = form.cleaned_data['first_name']
		surname = form.cleaned_data['surname']
		phone = form.cleaned_data['phone']
		buying_type = form.cleaned_data['buying_type']
		address = form.cleaned_data['address']
		user_email = form.cleaned_data['user_email']
		comments = form.cleaned_data['comments']
		new_order = Order()
		new_order.user = request.user
		new_order.save()
		new_order.items.add(cart)
		new_order.first_name = name
		new_order.surname = surname
		new_order.phone = phone
		new_order.buying_type = buying_type
		new_order.address = address 
		new_order.user_email = user_email
		new_order.comments = comments
		new_order.total = cart.catr_total
		new_order.save()
		del request.session['cart_id']
		del request.session['total']
		return HttpResponseRedirect(reverse('thank_you'))
	return render(request, 'order.html', {'categories': categories})



def account_view(request):
	categories = Category.objects.all()
	order =  Order.objects.filter(user=request.user).order_by('-id')
	context = {
	'order': order,
	'categories': categories
	}
	return render(request, 'account.html', context)


def registration_view(request):
	try:
		cart_id = request.session['cart_id']
		cart = Cart.objects.get(id=cart_id)
		request.session['total'] = cart.items.count()
	except:
		cart = Cart()
		cart.save()
		cart_id = cart.id
		request.session['cart_id'] = cart_id
		cart = Cart.objects.get(id=cart_id)
	form = RegistrationForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
			new_user = form.save(commit=False)
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			email    = form.cleaned_data['email']
			first_name = form.cleaned_data['first_name']
			last_name  = form.cleaned_data['last_name']
			new_user.username = username
			new_user.set_password(password)
			new_user.first_name = first_name
			new_user.last_name  = last_name
			new_user.email = email 
			new_user.save()
			login_user = authenticate(username=username, password=password)
			if login_user:
				login(request, login_user)
				return HttpResponseRedirect(reverse('base'))
	context ={
	'form':form,
	'categories': categories
	}
	return render(request, 'registration.html', context)

def login_view(request):
	form = LoginForm(request.POST or None)
	categories = Category.objects.all()
	if form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		login_user = authenticate(username=username, password=password)
		if login_user:														#перебрасывает на главную страницу если мы зашли ! 
			login(request, login_user)
			return HttpResponseRedirect(reverse('base'))
	context = {
		'form': form,
		'categories': categories
	}
	return render(request, 'login.html', context)

def logout_view(request):
	auth.logout(request)
	return HttpResponseRedirect('/')








		

# Create your views her
		