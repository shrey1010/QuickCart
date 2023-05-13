from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView, Token
)
from .views import *
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('register/',RegisterView.as_view(), name="registerview"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
   
]
