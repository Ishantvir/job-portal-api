from rest_framework import serializers
from .models import Skill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill 
        fields = ['id','name','created_at']
        read_only_fields = ['id','created_at']

    def validate_name(self,value):
        if not value.strip():
            raise serializers.ValidationError('Skill name cannot be empty or contain only whitespaces.')
        return value.strip()