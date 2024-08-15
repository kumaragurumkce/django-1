# myapp/views.py

from django.shortcuts import render, redirect,get_object_or_404
from .models import Image,Product,CategoryType,Contact,Profile
from .forms import ImageForm,ProductForm,ContactForm,UserRegisterForm,UserLoginForm,ProfileForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from decimal import Decimal, InvalidOperation

def image_upload(request):
    products=Product.objects.all()
    categories=CategoryType.objects.all()
    
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        print(form,'FORM.......')
        if form.is_valid():
            form.save()
            return redirect('home_content')
        else:
            (form.errors,'FORM ERRORS')
    else:
        form = ProductForm()
        
    context={
        'form': form,
        'products':products,
        'categories':categories
    }    
    return render(request, 'myapp/layout/product_form.html',context)


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            Profile.objects.create(user=user, user_type=Profile.CUSTOMER)
            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('home_content')
    else:
        user_form = UserRegisterForm()
    return render(request, 'myapp/layout/register.html', {'form': user_form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if Profile.objects.get(user=user).user_type == 'admin':
                return redirect('image_upload')
            else:
                return redirect('home_content')
    else:
        form = UserLoginForm()
    return render(request, 'myapp/layout/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')



def home_content(request):
    user = request.user
    # products = Product.objects.all()  # Replace with specific filtering if required

    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        # Handle the case where the user doesn't have a profile
        return HttpResponseNotFound("Profile not found")

    if profile.user_type == 1 or profile.user_type == 0:
        # Fetch products based on specific criteria if needed
        products1 = Product.objects.all()  # Replace with specific filtering if required
    print('not print',products1)
    return render(request, 'myapp/layout/home.html', {'images': products1})

def trends_page(request):
    trends_product=Product.objects.all().order_by('-id')
    print(trends_product,"trends")
    return render(request,'myapp/layout/trends.html',{'images':trends_product})

def about_page(request):
    return render(request,'myapp/layout/about.html')

def contact_page(request):
    form_submitted = request.GET.get('submitted', False)
    if request.method == 'POST':
        print("Form submitted")  # Debugging line
        contact = ContactForm(request.POST)
        if contact.is_valid():
            print("Form is valid")  # Debugging line
            contact.save()
            form_submitted = True
            return redirect(f"{request.path}?submitted=True")
    
    contact = ContactForm()
    return render(request, 'myapp/layout/contact.html', {'contact': contact, 'form_submitted': form_submitted})


login_required(login_url='login')
def addCart_page(request, pk):
    image = get_object_or_404(Product, pk=pk)
    print(image,'......................................................')
    cart = request.session.get('cart', [])
    print(image,"image......")
    if not isinstance(cart, list):
        cart = []
    item_in_cart=any(item['id']==image.id for item in cart)
    print(item_in_cart,'.......item_in_cart',)
    if item_in_cart:
        messages.warning(request,f'{image.product_name} is already in your cart!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # return render(request,'myapp/layout/home.html', {'images': Product.objects.all()})
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        
    cart.append({
        'id': image.id,
        'title': image.product_name,
        'image': image.image.url,
        'price_amount':str(image.price),
        
        # 'price':image.price
    })

    request.session['cart'] = cart
    print('cart',cart)
    messages.success(request, f'{image.product_name} has been added to your cart!')
    print(item_in_cart,'.......')
    
    return redirect('cartList_content')

def updateCart_page(request,pk):
    cart=get_object_or_404(Product,pk=pk)
    if request.method == 'POST':
        cart.product_name=request.POST.get('product_name',cart.product_name)
        if 'image' in request.FILES:
            cart.image = request.FILES['image']
        
        cart.save()  # Save the changes to the database
        print(cart.image,"......................................")
        # cart.save()
        return redirect('home_content')
    return render(request,'myapp/layout/updateCart.html',{'cart': cart})


def deleteCart_page(request, pk):
    cart = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        cart.delete()
        
        return redirect('cartlist')
    return render(request, 'myapp/layout/deleteCart.html', {'cart': cart})

def cartList_page(request):
    cart_array = request.session.get('cart', [])
    
    # Filter out duplicates and sort items
    unique_cart = {item['id']: item for item in cart_array}.values()
    cart = sorted(unique_cart, key=lambda item: item['id'], reverse=True)
    
    # Initialize the total price as Decimal
    total_price = Decimal('0.00')
    
    # Sum the price_amount values
    for item in cart:
        price_amount = item.get('price_amount', '0.00')  # Default to '0.00' if key is missing
        
        try:
            # Convert price_amount to Decimal and add to total_price
            total_price += Decimal(price_amount)
            total_price
            # Ensure price_amount is a valid numeric string
        except (ValueError, InvalidOperation):
            print(f"Invalid price value: {price_amount}")

    print(f"Total Price: {total_price}")
    print(cart,'cartitem')
    # Ensure 'context' is a dictionary
    context = {
        'cart': cart,
        'total_price': total_price
    }
    
    return render(request, 'myapp/layout/addcart.html', context)


def deleteCartItem(request, pk):
    cart = request.session.get('cart', [])
    
    # Filter out the item with the given pk
    cart = [item for item in cart if item['id'] != pk]
    
    # Update the session cart
    request.session['cart'] = cart
    messages.success(request, 'Item successfully removed from your cart.')
    print('delte'),cart
    return redirect('cartList_content') 

# def login_page(request):
#     if request.method == 'POST':
#         username=request.POST['username']
#         password=request.POST['password1']
#         user = authenticate(request,username=username,password=password)
#         if user is not None:
#             login(request,user)
#             return redirect('home_content')
#         else:
#             messages.error(request,'Invaid Username or password')
#     return render(request,'myapp/layout/login.html')

# def logout_page(request):
#     logout(request)
#     return redirect('login')

# def register_page(request):
#     if request.method == 'POST':
#         form_login = CustomerUserForm(request.POST)
#         if form_login.is_valid():
#             form_login.save()
#             username=form_login.cleaned_data.get('username')
#             password=form_login.cleaned_data.get('password1')
#             user=authenticate(username=username,password=password)
#             print('...')          
#             login(request,user)
#             return redirect('home_content')
#     else: 
#         form_login =CustomerUserForm()
#             # print(form,"form_else")
            
#     return render(request,'myapp/layout/register.html',{'form':form_login})





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
    categories = CategoryType.objects.all()
    context = {
        # 'products': products
        'categories': categories
    }
    print(categories,'.......categories')

    
    return render(request,'myapp/layout/product_list.html',context)

# Update an existing product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('image_upload')
    else:
        form = ProductForm(instance=product)
    return render(request, 'myapp/layout/product_form.html', {'form': form})

# Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('image_upload')
    return render(request, 'myapp/layout/product_delete.html', {'product': product})


def products_by_category(request, category_id):
    category = get_object_or_404(CategoryType, id=category_id)
    print(category,'caetgory........')
    products = Product.objects.filter(subcategory__category=category)
    print(products,'products........')
    return render(request, 'myapp/layout/category1.html', {'category': category, 'products': products})


