from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import auth
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password1'] and request.POST['password2']:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = User.objects.get(username=request.POST['email'])
                    return render(request, 'accounts/registration.html', {'error':'This email is already connected to an account'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['email'], password=request.POST['password1'])
                    user_profile = Profile()
                    user_profile.user = user
                    user_profile.email = request.POST['email']
                    user_profile.save()
                    auth.login(request,user)
                    return redirect('/')
            else:
                return render(request, 'accounts/registration.html', {'error':'Passwords must match'})
        else:
            return render(request, 'accounts/registration.html', {'error':'All fields must be filled'})
    else:
        return render(request, 'accounts/registration.html')

def login(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password1']:
            user = auth.authenticate(username=request.POST['email'], password=request.POST['password1'])
            if user is not None:
                auth.login(request, user)
                return redirect('accounts/mypage')
            else:
                return render(request, 'accounts/login.html', {'error': 'Password or email is incorrect'})
        else:
            return render(request, 'accounts/login.html', {'error':'You must fill all fields'})
    else:
        return render(request, 'accounts/login.html')

@login_required(login_url='accounts/login')
def mypage(request):

    context = {}
    return render(request, 'accounts/mypage.html', context)