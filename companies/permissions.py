from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsRecruiterAndOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return getattr(request.user, "role", None) == 'RECRUITER'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        recruiter_profile = getattr(request.user,'recruiter_profile',None)
        return obj.recruiter == recruiter_profile