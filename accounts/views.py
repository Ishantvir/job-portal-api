from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import userSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response(
                    {"error": "This account is disabled."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh' : str(refresh),
                    'access' : str(refresh.access_token)
                }, status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Invalid Email and Password"},
                 status.HTTP_401_UNAUTHORIZED,    
            )

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        return Response(
            {
                "email" : user.email,
                "is_active" : user.is_active,
                "message" : "You are successfully authenticated with JWT Token."
            }, status=status.HTTP_200_OK
        )