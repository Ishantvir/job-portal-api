from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.permissions import IsJobSeeker
from .models import Resume
from .serializers import ResumeSerializer

class ResumeView(APIView):
    permission_classes = [IsJobSeeker]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile = getattr(request.user, 'job_seeker_profile', None)
        if not profile:
            return Response({"error":"Job Seeker profile not found."}, status=status.HTTP_404_NOT_FOUND,)
        
        resume = getattr(profile, "resume", None)
        if not resume:
            return Response({"error":"No resume uploaded yet."}, status=status.HTTP_404_NOT_FOUND,)

        serializer = ResumeSerializer(resume)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print("FILES:", request.FILES)
        print("DATA:", request.data)
        profile = getattr(request.user, "job_seeker_profile", None)
        if not profile:
            return Response({'error':"Job Seeker profile not found"}, status=status.HTTP_404_NOT_FOUND,)

        existing_resume = getattr(profile, 'resume', None)
        if existing_resume:
            if existing_resume.file:
                existing_resume.file.delete(save=False)
            serializer = ResumeSerializer(existing_resume, data=request.data)
            status_code = status.HTTP_200_OK
        else:
            serializer = ResumeSerializer(data=request.data)
            status_code = status.HTTP_201_CREATED

        if serializer.is_valid():
            serializer.save(job_seeker=profile)
            return Response(serializer.data, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = getattr(request.user, "job_seeker_profile", None)
        resume = getattr(profile, "resume", None) if profile else None

        if not resume:
            return Response({"error": "No resume found to delete."}, status=status.HTTP_404_NOT_FOUND,)
        if resume.file:
            resume.file.delete(save=False)
        resume.delete()

        return Response({"message":"Resume delete successfully."},status=status.HTTP_204_NO_CONTENT,)

        