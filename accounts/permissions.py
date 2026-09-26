from rest_framework.permissions import BasePermission

class IsJobSeeker(BasePermission):
    
    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == 'JOB_SEEKER')
    
class IsRecruiter(BasePermission):

    def has_permission(self, request, view):
        return (request.user and request.user.is_authenticated and request.user.role == 'RECRUITER')