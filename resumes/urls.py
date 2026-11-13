from django.urls import path, include
from .views import ResumeView

urlpatterns = [
    path('resumes/',ResumeView.as_view(), name="job-seeker-resume"),
]
