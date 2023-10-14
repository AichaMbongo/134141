from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Profile, CustomUser, Patient, PatientDetails, DoctorPatientRel
# from django.contrib.admin import AdminSite
# from two_factor.admin import AdminSiteOTPRequiredMixin



admin.site.unregister(Group)

admin.site.unregister(User)


# class CustomAdminSite(AdminSiteOTPRequiredMixin, AdminSite):
#     pass

# custom_admin_site = CustomAdminSite(name='custom_admin')


# class PatientInline(admin.StackedInline):
#     model = PatientDetails

class PatientDetailsInline(admin.StackedInline):  # Use TabularInline for a more compact display
    model = PatientDetails

class PatientAdmin(admin.ModelAdmin):
    model = Patient
    inlines = [PatientDetailsInline]  # Use the modified inline
    list_display = ['firstName', 'lastName', 'email', 'phoneNo', 'sex']
    search_fields = ['firstName', 'lastName', 'email']
    


admin.site.register(Patient, PatientAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    inlines = [ProfileInline]
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
       
    )

# Register the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
     

admin.site.register(DoctorPatientRel)
# admin.site.register(User, UserAdmin)