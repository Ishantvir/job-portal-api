from rest_framework.permissions import BasePermission


class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False


class IsApplicationJobOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == "JOB_SEEKER":
            return obj.job_seeker == getattr(user, "job_seeker_profile", None)
        if user.role == "RECRUITER":
            return obj.job.company.recruiter == getattr(
                user, "recruiter_profile", None
            )
        return False