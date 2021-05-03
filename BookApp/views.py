from django.shortcuts import render, redirect

from BookApp.models import *
import bcrypt
from django.contrib import messages

def landingPage(request):
    return render(request, 'LandingPage.html')

def register(request):
    return render(request, 'Register.html')

def login(request):
    return render(request, 'Login.html')

def success(request):
    return render(request, 'ordersuccess.html')

def homePage(request):
    books = Book.objects.all()
    context = {
        'books': books
    }
    return render(request, 'Bookhomepage.html', context)

def cart(request):
    user = User.objects.get(id=request.session['user_id'])
    orders = Order.objects.all()

    context = {
        'user': user,
        'orders': orders
    }
    return render(request, 'Bookcart.html', context)

def edit(request):
    if 'user_id' not in request.session:
            return redirect('/')
    
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'ProfileEdit.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')

def registerUser(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/register')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/homePage')

def loginUser(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/login')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/homePage')

def editUser(request):
    errors = User.objects.editUser(request.POST)
    if request.method == "GET":
        return redirect('/homePage')
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/edit')
    edit_user = User.objects.get(id=request.session['user_id'])
    edit_user.first_name= request.POST['first_name']
    edit_user.last_name= request.POST['last_name']
    edit_user.email=request.POST['email']
    edit_user.username=request.POST['username']
    edit_user.password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    #edit_user.password=request.POST['password']
    #pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    edit_user.save()
    messages.success(request, "Updated!")
    return redirect('/edit')

def recentorders(request):
    user= User.objects.get(id=request.session['user_id'])
    orders = Order.objects.filter(user=user)
    context={ 
        "orders": orders
    }
    return render(request,"recentorder.html",context)    

def purchase(request,book_id):
    book= Book.objects.get(id=book_id)
    user= User.objects.get(id=request.session['user_id'])
    order=Order(user=user,book=book)
    order.save()
    messages.success(request, "Book added to cart!")
    return redirect('/homePage')

def viewbook(request,book_id):
   thebook= Book.objects.get(id=book_id)
   context={
       "thebook":thebook
   } 
   return render(request,"bookinfo.html",context)

def checkout(request):
    orders = Order.objects.all()
    orders.delete()
    return redirect('/success')

def delete(request):
    orders = Order.objects.all()
    orders.delete()
    messages.success(request, "Books deleted!")
    return redirect('/homePage')