from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class RegisterView(APIView):

    def post(self, request):
        username = request.GET.get("username")
        password = request.GET.get("password")
        user = User.objects.get(username=username),
        user.set_password(password)
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({"status": 200,
                        "mssg": "user registration successful", 
                        'refresh': str(refresh),
                        'access': str(refresh.access_token), })
