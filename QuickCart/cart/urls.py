from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('cart/', CartView.as_view()),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('payment-callback/', PaymentCallbackView.as_view(),name='payment-callback'),
]
