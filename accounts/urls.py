from django.urls import path, include

from .views import RegisterView, LoginView, UserProfileView, JobSeekerProfileView, RecruiterProfileView


urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('job-seeker/profile/', JobSeekerProfileView.as_view(), name="job-seeker-profile"),
    path('recruiter/profile/', RecruiterProfileView.as_view(), name="recruiter-profile"),
]
