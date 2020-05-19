from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registration),
    path('login/', views.login),
    path('mypage/', views.mypage),
]
