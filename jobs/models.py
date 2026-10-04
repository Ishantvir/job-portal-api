from django.db import models
from companies.models import Company

class Job(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full Time'
        PART_TIME = 'PART_TIME', 'Part Time'
        CONTRACT = 'CONTRACT', 'Contract'
        INTERNSHIP = 'INTERNSHIP','Internship'
        REMOTE = 'REMOTE', 'Remote'

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')

    title = models.CharField(max_length=255)
    description = models.TextField()

    location = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(max_length=20, choices=JobType.choices, default=JobType.FULL_TIME,)

    salary_min = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    experience_required = models.PositiveIntegerField(default=0, help_text="Required Experience in Years.")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} at {self.company}'

    