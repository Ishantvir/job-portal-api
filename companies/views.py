from rest_framework import viewsets

from .permissions import IsRecruiterAndOwnerOrReadOnly
from .serializers import CompanySerializer
from .models import Company


class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsRecruiterAndOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(recruiter = self.request.user.recruiter_profile)