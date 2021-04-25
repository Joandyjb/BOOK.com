from django.urls import path

from . import views
urlpatterns = [
    path('', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('registerUser', views.registerUser),
    path('loginUser', views.loginUser),
    path('landingPage', views.landingPage)
]
