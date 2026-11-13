from rest_framework import serializers
from .models import User, JobSeekerProfile, RecruiterProfile
from skills.models import Skill
from skills.serializers import SkillSerializer

class userSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id','email','role', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True, 
                'style': {'input_type': 'password'}
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user

class JobSeekerProfileSerializer(serializers.ModelSerializer):
    skills_details = SkillSerializer(source="skills", many=True, read_only=True)
    skills = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), many=True, write_only=True, required=False)
    
    class Meta:
        model = JobSeekerProfile
        fields = ['id','phone','location', 'skills_details','skills','bio']

class RecruiterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterProfile
        fields = ['id','phone','designation']