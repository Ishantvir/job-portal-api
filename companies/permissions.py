from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRecruiterAndOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return (request.user and request.user.is_authenticated and request.user.role == 'RECRUITER')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.recruiter == getattr(request.user, 'recruiter_profile', None)