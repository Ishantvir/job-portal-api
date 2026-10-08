from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job 
        fields = ["id", "company","title","description","location","job_type","salary_min","salary_max","experience_required","is_active","created_at","updated_at"]
        read_only_fields = ['id','created_at','updated_at']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Title cannot be empty and contain space only.')
        return value

    def validate_salary_min(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('Minimum salary cannot be negative.')
        return value
    
    def validate_salary_max(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError('Maximim salary cannot be negative.')
        return value

    def validate_experience_required(self, value):
        if value < 0:
            raise serializers.ValidationError('Required experience cannot be negative.')
        return value

    def validate(self, attrs):
        salary_min = attrs.get('salary_min') if 'salary_min' in attrs else getattr(self.instance, 'salary_min', None)
        salary_max = attrs.get('salary_max') if 'salary_max' in attrs else getattr(self.instance, 'salary_max', None)

        if salary_min is not None and salary_max is not None:
            if salary_min > salary_max:
                raise serializers.ValidationError({'salary_min':'Minimum salary should not greater than Maximin salary'})
        return attrs