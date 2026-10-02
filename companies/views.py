from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from .permissions import IsRecruiterAndOwnerOrReadOnly
from .serializers import CompanySerializer
from .models import Company


class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsRecruiterAndOwnerOrReadOnly]

    def perform_create(self, serializer):
        recruiter_profile = getattr(self.request.user, "recruiter_profile", None)
        if not recruiter_profile:
            raise PermissionDenied("Your account is missing an active Recruiter Profile layout.")
        serializer.save(recruiter=recruiter_profile)