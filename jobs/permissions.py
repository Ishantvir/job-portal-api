from rest_framework.permissions import BasePermission, SAFE_METHODS
from companies.models import Company

class IsRecruiterAndOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True


        if request.method == "POST":
            company_id = request.data.get("company")
            if not company_id:
                return False
            try:
                company = Company.objects.get(id=company_id)
                recruiter_profile = getattr(request.user, "recruiter_profile", None)
                return (recruiter_profile is not None and company.recruiter == recruiter_profile)
            except Company.DoesNotExist:
                return False

        return getattr(request.user, "role", None) == "RECRUITER"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        recruiter_profile = getattr(request.user, "recruiter_profile", None)
        return recruiter_profile is not None and obj.company.recruiter == recruiter_profile