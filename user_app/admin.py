from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .models import Profile, CustomUser, Patient, PatientDetails, DoctorPatientRel, TreatmentPlan, Appointment, PredictionResult, HeartDiseasePrediction
# from django.contrib.admin import AdminSite
# from two_factor.admin import AdminSiteOTPRequiredMixin



# Include your custom CSS


# admin.site.unregister(Group)

# Create groups
# Group.objects.create(name='Admin')
# Group.objects.create(name='Secretaries')
# Group.objects.create(name='Nurses')
# Group.objects.create(name='Doctors')
# Group.objects.create(name='Unassigned')

admin.site.unregister(User)


# class CustomAdminSite(AdminSiteOTPRequiredMixin, AdminSite):
#     pass

# custom_admin_site = CustomAdminSite(name='custom_admin')


# class PatientInline(admin.StackedInline):
#     model = PatientDetails

class PatientDetailsInline(admin.StackedInline):  # Use TabularInline for a more compact display
    model = PatientDetails
    
    
class HeartDiseasePredictionInline(admin.StackedInline):
    model = HeartDiseasePrediction

class TreatmentInline(admin.StackedInline):  # Use TabularInline for a more compact display
    model = TreatmentPlan

class PredictionInline(admin.StackedInline):  # Use TabularInline for a more compact display
    model = PredictionResult  
    extra = 0  # This ensures no extra empty forms are displayed by default
    readonly_fields = ['date']  # Make the date field read-only

class PatientAdmin(admin.ModelAdmin):
    model = Patient
    inlines = [PatientDetailsInline, TreatmentInline, PredictionInline, HeartDiseasePredictionInline]  # Use the modified inline
    list_display = ['firstName', 'lastName', 'email', 'phoneNo', 'sex']
    search_fields = ['firstName', 'lastName', 'email']

    


admin.site.register(Patient, PatientAdmin)

class ProfileInline(admin.StackedInline):
    model = Profile

class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    inlines = [ProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role_display', 'is_active')

    def get_role_display(self, obj):
        if hasattr(obj, 'profile') and obj.profile:
            return obj.profile.get_role_display()
        return None

    get_role_display.short_description = 'Role'

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register the CustomUserAdmin
admin.site.register(User, CustomUserAdmin)
     

admin.site.register(DoctorPatientRel)

admin.site.register(Appointment)
# admin.site.register(User, UserAdmin)

