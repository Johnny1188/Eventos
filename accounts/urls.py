from django.urls import path, include
from . import views

urlpatterns = [
    path('signup/', views.registration,name="registration"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name='logout'),
    path('deleteaccount/<int:userid>/', views.deleteAccount, name='deleteaccount'),
    path('', include('allauth.urls')),
    path('profile/', views.oauthRedirect,name="redirect"),
]
