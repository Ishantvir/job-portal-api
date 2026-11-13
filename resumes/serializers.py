import os
from rest_framework import serializers
from .models import Resume

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ['id', 'file','created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_file(self, value):
        ext = os.path.splitext(value.name)[1].lower()
        valid_extensions = ['.pdf', '.doc', '.docx']
        if ext not in valid_extensions:
            raise serializers.ValidationError('Unsupported file format. Only PDF, DOC, DOCX files are allowed.')

        max_size = 5*1024*1024
        if value.size > max_size:
            raise serializers.ValidationError('File Size cannot exceed 5 MB')
        return value