from django.urls import path, include
from . import views

urlpatterns = [
    path('registration/', views.registration,name="registration"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('deleteaccount/<int:userid>/', views.deleteAccount, name='deleteaccount'),
]
