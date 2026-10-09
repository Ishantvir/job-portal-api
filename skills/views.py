from rest_framework import viewsets
from .models import Skill
from .serializers import SkillSerializer
from .permissions import IsRecruiterOrReadOnly

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsRecruiterOrReadOnly]