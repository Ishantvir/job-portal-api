from rest_framework import viewsets,status
from rest_framework.exceptions import PermissionDenied

from .models import Job
from .serializers import JobSerializer
from .permissions import IsRecruiterAndOwnerOrReadOnly

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterAndOwnerOrReadOnly]

    def perform_update(self, serializer):
        new_company = serializer.validated_data.get("company")
        recruiter_profile = getattr(self.request.user, "recruiter_profile", None)

        if new_company and new_company.recruiter != recruiter_profile:
            raise PermissionDenied("You Cannot Assign This Job to a Company you donot own.")

        serializer.save()