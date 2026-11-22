from rest_framework import serializers
from jobs.models import Job
from .models import Application 

class JobSummarySerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source = "company.name", read_only=True)

    class Meta:
        model = Job
        fields = ["id","title","company_name","location"]

class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), write_only = True,)
    job_details = JobSummarySerializer(source='job', read_only=True)

    class Meta:
        model = Application
        fields = ["id","job", "job_details","cover_letter","status","applied_at","updated_at",]
        read_only_fields = ["id","status","applied_at","updated_at",]

    def validate_job(self,value):
        if not value.is_active:
            raise serializers.ValidationError('You cannot apply to a job is no longer active.')
        return value

    def validate(self,attrs):
        request = self.context.get('request')
        job = attrs.get('job')

        if request and hasattr(request.user, "job_seeker_profile") and job:
            profile = request.user.job_seeker_profile
            if Application.objects.filter(job_seeker=profile, job=job).exists():
                    raise serializers.ValidationError({'job':'You have already applied for this job.'})
        return attrs

class RecruiterApplicationSerializer(serializers.ModelSerializer):
    applicant_email = serializers.EmailField(source='job_seeker.user.email', read_only=True)
    job_title = serializers.CharField(source = 'job.title', read_only=True)
    company_name = serializers.CharField(source='job.company.name', read_only = True)

    class Meta:
        model = Application
        fields = ["id", "applicant_email", "job", "job_title", "company_name", "cover_letter", "status", "applied_at","updated_at",]
        read_only_fields = ["id", "applicant_email", "job", "job_title", "company_name", "cover_letter", "applied_at","updated_at",]