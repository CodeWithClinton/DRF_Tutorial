from ast import Add
from gettext import install
import re
from django.shortcuts import render, redirect
from .models import Product, Cart, Cartitems, Category, SavedItem
from django.http import JsonResponse
from django.core import serializers
from . forms import AddressForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
import uuid
from UserProfile.models import Address
from .forms import UpdateUserForm
from django.db.models import Q
# Create your views here.


def index(request):
    # try:
    #     cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    # except:
    #     request.session['nonuser'] = str(uuid.uuid4())
    #     cart = Cart.objects.create(session_id = request.session['nonuser'], completed=False)
        
    top_deal = Product.objects.filter(discount=True)
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {'top_deals': top_deal, 'categories':categories, 'products':products }
    
    return render(request, 'storeapp/index.html', context)

def category(request, slug):
    category = Category.objects.get(slug=slug)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'storeapp/category.html', context)
    

def detail(request, slug):
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    product = Product.objects.get(slug=slug)
    similar_products = Product.objects.filter(category= product.category).exclude(slug=product.slug)
    counter = 0
    recently_viewed_products = None
    try:
        saveitem = SavedItem.objects.get(product=product)
        counter = 1
    except:
        saveitem = None
    if 'recently_viewed' in request.session:
        if slug in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(slug)
        
        recently_viewed_products = Product.objects.filter(slug__in = request.session['recently_viewed'])
        request.session['recently_viewed'].insert(0, slug)
        if len(request.session['recently_viewed']) > 5:
            request.session['recently_viewed'].pop()
    
    else:
        request.session['recently_viewed'] = [slug]
    
    request.session.modified = True
    print(counter)
    context = {'product': product, 'cart': cart, 'saveitem': saveitem,
               'counter': counter, 'recently_viewed_products':recently_viewed_products, 'similar_products': similar_products}
    return render(request, 'storeapp/detail.html', context)


def cart(request):
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems = cart.cartitems_set.all()
    context = {'cart':cart, 'cartitems': cartitems}
    return render(request, 'storeapp/cart.html', context)


def updateCart(request):
    data = json.loads(request.body)
    pro_id = data['p_id']
    action = data['action']
    product = Product.objects.get(id=pro_id)
    
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)
    
    if action == 'add':
        cartitems.quantity += 1
    cartitems.save()
    
    
    msg = {
        'num_of_items': cart.num_of_items
    }
    return JsonResponse(msg, safe = False)

def updateQuantity(request):
    data = json.loads(request.body)
    product_id = data['id']
    quantity = data['qty']
    price = data['product_price']
    product = Product.objects.get(id=product_id)
   
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)
    cartitems.quantity = quantity
    if int(cartitems.quantity) == 0:
        cartitems.delete()
    cartitems.save()
    msg = {
        'num': cart.num_of_items,
        'qty': quantity,
        'price': price,
        'total': cart.cart_total
    }
   
    return JsonResponse(msg , safe=False)

def deleteCartitems(request):
    data = json.loads(request.body)
    # customer = request.user.customer
    product_id = data['id']
    product = Product.objects.get(id=product_id)
    # cart, created = Cart.objects.get_or_create(owner=customer, completed=False)
    # cartitems, created = Cartitems.objects.get_or_create(product=product, cart=cart)
    
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems = Cartitems.objects.filter(product=product, cart=cart)
    print(cartitems)
    cartitems.delete()
    # cartitems.save()    # if cartitems:
    #     print('mmmdkd')
    #     cartitems.delete()
    #     cartitems.save()
    return JsonResponse(str(cartitems), safe=False)

@login_required(login_url='signin')
def checkout(request):
    form = None
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    cartitems = cart.cartitems_set.all()
    customer = request.user.customer
    customer_address = Address.objects.filter(customer=customer)
    if customer_address:
        print(customer_address)
    else:
        form = AddressForm()
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.customer = request.user.customer
                address.save()
                
                messages.info(request, 'Shipping info saved')
    
    context = {'cart': cart, 'form':form,'cartitems':cartitems, 'customer_address': customer_address}
    return render(request, 'storeapp/checkout.html', context)

@login_required(login_url='signin')
def account(request):
    customer = request.user.customer
    address = Address.objects.filter(customer=customer)
    context = {'customer': customer, 'address':address}
    return render(request, 'storeapp/account.html', context)

@login_required(login_url='signin')
def confirmPayment(request):
    data = json.loads(request.body)
    total = float(data['total'])
    print(total)
    cart = Cart.objects.get(session_id = request.session['nonuser'], completed=False)
    print(cart.cart_total)
    if total == cart.cart_total:
        cart.completed = True
    else:
        messages.info(request, 'There is an issue with your purchase')
    cart.save()
    return JsonResponse('it is workking', safe=False)

@login_required(login_url='signin')
def saveItems(request):
    customer = request.user.customer
    saveitems = SavedItem.objects.filter(owner=customer)
    context = {'saveitems':saveitems}
    return render(request, 'storeapp/saveitem.html', context)


@login_required(login_url='signin')
def order(request):
    customer = request.user.customer
    orders = Cart.objects.filter(owner=customer)
    context = {'orders':orders}
    return render(request, 'storeapp/order.html', context)


@login_required(login_url='signin')
def addSavedItems(request):
    if request.method=='POST':
        saveitems = None
        customer = request.user.customer
        data = json.loads(request.body)
        counter = data['counter']
        product_id = data['d']
        product = Product.objects.get(id=product_id)
        saveitems, created= SavedItem.objects.get_or_create(owner=customer, product=product)
        saveitems.added = 1
        saveitems.save()
        
        if counter == 0:
            new_counter = 0
            saveitems = SavedItem.objects.filter(owner=customer, product=product)
            saveitems.delete()
  
    if saveitems:
        print('mmmmmm')
        new_counter = 1
    else:
        print('00000000')
        new_counter = 0
    # print(new_counter)
    return JsonResponse(new_counter, safe=False)
 
def update_user_info(request):
    customer = request.user.customer
    form = UpdateUserForm(instance=customer)
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect ('account')
    context = {'form': form}
    return render(request, 'storeapp/update_user.html', context)
    

def search(request):
    search_query = request.GET.get('search_query')
    products = Product.objects.filter(Q(name__icontains=search_query) | Q(category__title__icontains = search_query))
    context = {'products': products, 'search_query':search_query}
    return render(request, 'storeapp/search.html', context)