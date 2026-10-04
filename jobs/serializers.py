from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job 
        fields = ["id", "company","title","description","location","job_type","salary_min","salary_max","experience_required","is_active","created_at","updated_at"]
        read_only_fields = ['id','created_at','updated_at']