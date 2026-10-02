from django.db import models
from accounts.models import RecruiterProfile

class Company(models.Model):
    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='companies')

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True,null=True)
    location = models.CharField(max_length=255,blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)