from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated is False:
        return render(request,"home.html")
    else:
        finalUrl = '/rew/mypage/'+ str(request.user.id) +'/'
        return redirect(finalUrl)