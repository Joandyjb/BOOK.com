from django.shortcuts import render, redirect

from BookApp.models import *
import bcrypt
from django.contrib import messages

def register(request):
    return render(request, 'Register.html')

def login(request):
    return render(request, 'Login.html')

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

def landingPage(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'LandingPage.html', context)

def registerUser(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/landingPage')

def loginUser(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/login')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/landingPage')

def editUser(request):
    errors = User.objects.editUser(request.POST)
    if request.method == "GET":
        return redirect('/landingPage')
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
