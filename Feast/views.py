from django.shortcuts import render,redirect
from .forms import MenuForm
from .models import CustomUser,Menu,Cart
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib import messages
# import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import os
# from dotenv import load_dotenv
# load_dotenv()
# Create your views here.
@login_required(login_url='login')
def add_menu(request):
    if not request.user.is_staff:  
        return HttpResponseForbidden("You are not authorized to view this page.")
    form = MenuForm()
    if request.method =="POST":
        form = MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('addmenu')
        else:
            form = MenuForm()
    context = {
        "form":form
    }
    return render(request,"addmenu.html",context)

def signupview(request):
    errors = {}
    logged_in_user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print(username, "llllllllllllll")
        print(email)
        print(password)
        print(confirm_password)


        if logged_in_user.is_staff:  
             if username == "anu":
                username = "anu"  
             if email == "anu@gmail.com":
                email = "anu@gmail.com"  

    
        if CustomUser.objects.filter(username=username).exclude(username='anu').exists():
            errors['username'] = "Username is already taken"
            return render(request, 'signup.html', {'errors': errors})

    
        if CustomUser.objects.filter(email=email).exclude(email='anu@gmail.com').exists():
            errors["email"] = "Email is already taken"
            return render(request, 'signup.html', {'errors': errors})


        
        if password != confirm_password:
            errors["confirm_password"] = "Passwords do not match!"

    
        if errors:
            return render(request, 'signup.html', {'errors': errors})

        # # Create a new user if no errors
        # user = CustomUser.objects.create_user(email=email, username=username, password=password)
        # user.set_password(password)  # Hash the password
        # user.save()

        # # After user is created, redirect to the login page
        # messages.success(request, 'Account created successfully! You can now log in.')
        # return redirect('login')
        try:
            user = CustomUser.objects.create_user(email=email, username=username, password=password)
            user.set_password(password)  # Hash the password
            user.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')

        except Exception as e:
            errors["server"] = "An error occurred while creating the user: " + str(e)
            return render(request, 'signup.html', {'errors': errors})

    return render(request, 'signup.html')

def signinview(request):
    if request.method == 'POST':
        errors = {}
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=user_name, password=password)

        if user is None:
            errors["user"] = "User does not exist"
        
        if errors:
            return render(request, "signin.html", {'errors': errors})
        else:
            login(request, user)
            messages.success(request, 'Login successful')

            # Check if the user is an admin (staff)
            if user.is_staff:  # Admin user
                return redirect('addmenu')  # Admin goes to the add product page
            else:  # Regular customer
                return redirect('menulist')  # Customer goes to the product list page

    return render(request, 'signin.html')

def signoutview(request):   
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')
def home_view(request):
   return render(request,'home.html',{'user':request.user})
def main_view(request):
   return render(request,'main.html',{'user':request.user})
@login_required(login_url='login')
def menulist(request):
    pdt = None
    try:
        searching = request.GET.get('query', '')
        if searching:
            pdt = Menu.objects.filter(fooditem__icontains=searching)
            print(pdt,"111111111111")
        else:
            pdt = Menu.objects.all()
        
        return render(request, 'menulist.html', {'menu': pdt})
    except Exception:
        return render(request, 'menulist.html', {'menu': pdt})

def menu_delete(request,id):
    Menu_item=Menu.objects.get(id=id)
    Menu_item.delete()
    messages.success(request,'menu deleted successfully')
    return redirect('menulist')
def menu_edit(request,id):
    Menu_item=Menu.objects.get(id=id)
    if request.method == "POST":
        form = MenuForm(request.POST, request.FILES, instance=Menu)
        if form.is_valid():
            form.save()
            return redirect('menulist')
    else:
        form = MenuForm(instance=Menu)
    return render(request,'editmenu.html',{'menu':Menu,'form':form})
@login_required(login_url='login')
def add_to_cart(request, menu_id):
    Menu= Menu.objects.get(id=menu_id)
    user = request.user

    # Check if the product is already in the user's cart
    cart_item, created = Cart.objects.get_or_create(user=user, menu=Menu)

    if not created:
        # If item already exists, update the quantity
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'{Menu.fooditem} added to cart!')
    return redirect('menulist')
@login_required(login_url='login')
def view_cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    return render(request, 'addcart.html', {'cart_items': cart_items})
    
