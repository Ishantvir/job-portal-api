from django.db import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import NotFound, ValidationError
from accounts.permissions import IsJobSeeker
from .models import Application
from .serializers import ApplicationSerializer

class ApplicationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsJobSeeker]

    def get_queryset(self):
        profile = getattr(self.request.user, "job_seeker_profile", None)
        if not profile:
            return Application.objects.none()

        return Application.objects.filter(job_seeker=profile).select_related('job','job__company')

    def perform_create(self, serializer):
        profile = getattr(self.request.user, "job_seeker_profile", None)
        if not profile:
            raise NotFound('Job Seeker profile not found.')

        try:
            serializer.save(job_seeker = profile)
        except IntegrityError:
            raise ValidationError({'job':'You have already applied for this job.'})
