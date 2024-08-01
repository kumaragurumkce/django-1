# myapp/views.py

from django.shortcuts import render, redirect,get_object_or_404
from .models import Image,Product,CategoryType
from .forms import ImageForm,CustomerUserForm,ProductForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def image_list(request, category=None):
    images = Image.objects.all().order_by('-id')
    # if category:
    #     images = images.filter(category=category)
    #     print(category,">>>>>>>>>>>>>>>>>>>")
    return render(request, 'myapp/layout/img_list.html', {'images': images, 'category': category})

def image_upload(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('image_list')
    else:
        form = ImageForm()
    return render(request, 'myapp/layout/img_upload.html', {'form': form})


def home_content(request):
    # home_images=Image.objects.filter(category='home').order_by('-id')
    products = Product.objects.all()
    
    return render(request,'myapp/layout/home.html',{'images':products})


def collections_page(request):
    collections_images=Image.objects.filter(category='collections').order_by('-id')
    return render(request,'myapp/layout/collections.html',{'images': collections_images})


def trends_page(request):
    trends_images=Image.objects.filter(category='trends').order_by('-id')
    return render(request,'myapp/layout/trends.html',{'images':trends_images})

def about_page(request):
    return render(request,'myapp/layout/about.html')

def contact_page(request):
    return render(request,'myapp/layout/contact.html')

login_required(login_url='login')
def addCart_page(request, pk):
    image = get_object_or_404(Image, pk=pk)
    cart = request.session.get('cart', [])

    if not isinstance(cart, list):
        cart = []

    # Add the item to the cart
    cart.append({
        'id': image.id,
        'title': image.title,
        'image': image.image.url  # Ensure this field is correct
    })

    request.session['cart'] = cart
    
    return redirect('cartList_content')

def updateCart_page(request,pk):
    cart=get_object_or_404(Image,pk=pk)
    if request.method == 'POST':
        cart.title=request.POST.get('title',cart.title)
        if 'image' in request.FILES:
            cart.image = request.FILES['image']
        
        cart.save()  # Save the changes to the database
        print(cart.image,"......................................")
        # cart.save()
        return redirect('home_content')
    return render(request,'myapp/layout/updateCart.html',{'cart': cart})


def deleteCart_page(request, pk):
    cart = get_object_or_404(Image, pk=pk)
    if request.method == 'POST':
        cart.delete()
        return redirect('cartlist')
    return render(request, 'myapp/layout/deleteCart.html', {'cart': cart})

def cartList_page(request):
    cart_array = request.session.get('cart', [])
    
    # Use a dictionary to filter duplicates by product ID
    unique_cart = {item['id']: item for item in cart_array}.values()
    
    cart = sorted(unique_cart, key=lambda item: item['id'],reverse=True)
    print(cart,'Cart++++++++++++')
    return render(request,'myapp/layout/addcart.html',{'cart':cart})

def deleteCartItem(request, pk):
    cart = request.session.get('cart', [])
    
    # Filter out the item with the given pk
    cart = [item for item in cart if item['id'] != pk]
    
    # Update the session cart
    request.session['cart'] = cart
    
    return redirect('cartList_content') 

def login_page(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password1']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home_content')
        else:
            messages.error(request,'Invaid Username or password')
    return render(request,'myapp/layout/login.html')

def logout_page(request):
    logout(request)
    return redirect('login')

def register_page(request):
    if request.method == 'POST':
        form_login = CustomerUserForm(request.POST)
        if form_login.is_valid():
            form_login.save()
            username=form_login.cleaned_data.get('username')
            password=form_login.cleaned_data.get('password1')
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('home')
    else: 
        form_login =CustomerUserForm()
            # print(form,"form_else")
            
    return render(request,'myapp/layout/register.html',{'form':form_login})


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'myapp/layout/product_form.html', {'form': form})

# Read a list of products
def product_list(request):
    products = Product.objects.all()
    categories = CategoryType.objects.all()
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'myapp/layout/product_list.html', context)

# Update an existing product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/layout/product_form.html', {'form': form})

# Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'myapp/layout/product_delete.html', {'product': product})


def products_by_category(request, category_id):
    category = get_object_or_404(CategoryType, id=category_id)
    print(category,'caetgory........')
    products = Product.objects.filter(subcategory__category=category)
    print(products,'products........')
    return render(request, 'myapp/layout/category1.html', {'category': category, 'products': products})