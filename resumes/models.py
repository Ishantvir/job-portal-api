from django.db import models
from accounts.models import JobSeekerProfile

# Create your models here.
class Resume(models.Model):
    job_seeker = models.OneToOneField(
        JobSeekerProfile, 
        on_delete=models.CASCADE, 
        related_name="resume",
    )
    file = models.FileField(upload_to="resumes/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Resume: {self.job_seeker.user.email}"