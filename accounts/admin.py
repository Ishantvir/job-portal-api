from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, JobSeekerProfile, RecruiterProfile
from .forms import CustomUserChangeForm, CustomUserCreationForm

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    add_form = CustomUserCreationForm
    
    form = CustomUserChangeForm

    list_display = ('email','role','is_staff','is_active')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields' : ('email','password')}),
        ('Personal info', {'fields': ('first_name', 'last_name','role',),}),
        ('Permissions', {'fields' : ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),}),
        ("Important dates", {"fields" : ("last_login", "date_joined"),}),
    )
    
    add_fieldsets = (
        (None, {
            'classes' : ('wide',), 
            'fields' : ('email','role','password1', 'password2')
        }),
    )

@admin.register(JobSeekerProfile)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ('phone', 'location', 'bio')

@admin.register(RecruiterProfile)
class RecruiterAdmin(admin.ModelAdmin):
    list_display = ('phone', 'designation')

