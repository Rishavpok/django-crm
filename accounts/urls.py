from os import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home , name='home' ),
    path('product/', views.product_data , name='product'),
    path('customer/<str:pk_test>', views.customer, name='customer'),
    path('create_order/<str:pk>/', views.create_order , name='create_order'),
    path('update_order/<str:pk>', views.update_order , name='update_order'),
    path('delete_order/<str:pk>', views.delete_order , name='delete_order')
]