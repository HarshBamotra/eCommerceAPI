from django.urls import path
from seller import views

urlpatterns = [
    path('', views.test),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('me/', views.me),
    path('product/', views.products),
    path('product/manage/', views.product),
]
