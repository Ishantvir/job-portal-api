from django.shortcuts import render
from django.contrib.auth import authenticate

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import userSerializer, JobSeekerProfileSerializer, RecruiterProfileSerializer
from .models import User, JobSeekerProfile, RecruiterProfile
from .permissions import IsJobSeeker, IsRecruiter


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = userSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

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
                "role" : user.role,
                "is_active" : user.is_active,
                "message" : "You are successfully authenticated with JWT Token."
            },
            status=status.HTTP_200_OK
        )

class JobSeekerProfileView(APIView):
    permission_classes = [IsJobSeeker]

    def get(self, request):
        profile = getattr(request.user, 'job_seeker_profile', None)
        if profile:
            return Response(JobSeekerProfileSerializer(profile).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
class RecruiterProfileView(APIView):
    permission_classes = [IsRecruiter]

    def get(self, request):
        profile = getattr(request.user, 'recruiter_profile', None)
        if profile:
            return Response(RecruiterProfileSerializer(profile).data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)