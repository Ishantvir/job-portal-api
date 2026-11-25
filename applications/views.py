from django.db import IntegrityError
from rest_framework import mixins, status, viewsets
from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsJobSeeker, IsRecruiter
from rest_framework.views import APIView
from .permissions import IsApplicationJobOwner, DenyAll
from .models import Application
from .serializers import ApplicationSerializer, RecruiterApplicationSerializer

class ApplicationViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,viewsets.GenericViewSet):

    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    def get_permissions(self):
        if self.action == "create":
            return [IsJobSeeker()]
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        if self.action == "partial_update":
            return [IsRecruiter(), IsApplicationJobOwner()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if getattr(self.request.user, "role", None) == 'RECRUITER':
            return RecruiterApplicationSerializer
        return ApplicationSerializer
        
    def get_queryset(self):
        user = self.request.user
        base_qs = Application.objects.select_related("job", "job__company", "job_seeker__user",)
        
        if user.role == "JOB_SEEKER":
            profile = getattr(user, "job_seeker_profile", None)
            if not profile:
                return Application.objects.none()
            return base_qs.filter(job_seeker = profile)
        
        if user.role == "RECRUITER":
            recruiter_profile = getattr(user, "recruiter_profile", None)
            if not recruiter_profile:
                return Application.objects.none()
            return base_qs.filter(job__company__recruiter = recruiter_profile)

        return Application.objects.none()

    def perform_create(self, serializer):
        profile = getattr(self.request.user, "job_seeker_profile", None)
        if not profile:
            raise NotFound('Job Seeker profile not found.')

        try:
            serializer.save(job_seeker = profile)
        except IntegrityError:
            raise ValidationError({'job':'You have already applied for this job.'})


