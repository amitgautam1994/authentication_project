from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout),
    path('reset_password/', views.reset_password),
]