from django.urls import path

from . import views
urlpatterns = [
    path('', views.landingPage),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('registerUser', views.registerUser),
    path('loginUser', views.loginUser),
    path('editUser', views.editUser),
    path('edit', views.edit),
    path('homePage', views.homePage),
    path('recentorders', views.recentorders),
    path('purchasebook/<book_id>', views.purchase),
]
