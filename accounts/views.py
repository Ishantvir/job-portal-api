from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import userSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializer
    permission_classes = [AllowAny]