from django.urls import path
from buyer import views

urlpatterns = [
    path('', views.test),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
    path('me/', views.me),
    path('buy/', views.buy)
]
