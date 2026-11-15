from django.db import models
from accounts.models import JobSeekerProfile
from jobs.models import Job

class Application(models.Model):
    class Status(models.TextChoices):
        APPLIED = "APPLIED", "Applied"
        SHORTLISTED = "SHORTLISTED", "Shortlisted"
        INTERVIEW = "INTERVIEW", "Interview"
        SELECTED = "SELECTED", "Selected"
        REJECTED = "REJECTED", 'Rejected'

    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='applications',)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications',)

    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.APPLIED,)

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['job_seeker','job'], name='unique_job_seeker_application',)]
        ordering = ['-applied_at']

    def __str__(self):
        return f'{self.job_seeker.user.email} -> {self.job.title} ({self.status})'
