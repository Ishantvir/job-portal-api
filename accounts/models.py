from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.conf import settings

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    class Role(models.TextChoices):
        JOB_SEEKER = "JOB_SEEKER", "Job Seeker"
        RECRUITER = "RECRUITER", "Recruiter"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_seeker_profile")

    phone = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True,null=True)

    skills = models.ManyToManyField("skills.Skill", related_name='job_seeker', blank=True)

    def __str__(self):
        return f'Profile: {self.user.email}'

class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')

    phone = models.CharField(max_length=15, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. HR Manager, Tech Lead")

    def __str__(self):
        return f'Profile: {self.user.email}'
    

