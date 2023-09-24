from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import User, Patient, Prediction, UserRole, DoctorPatientRel, TreatmentPlan, Role, PatientDetails, Report, Profile

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# from .models import UserProfile

# Define your custom list filters
class StaffStatusFilter(admin.SimpleListFilter):
    title = 'Staff Status'
    parameter_name = 'is_staff'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_staff=True)
        if self.value() == 'no':
            return queryset.filter(is_staff=False)

class SuperuserStatusFilter(admin.SimpleListFilter):
    title = 'Superuser Status'
    parameter_name = 'is_superuser'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_superuser=True)
        if self.value() == 'no':
            return queryset.filter(is_superuser=False)

class ActiveStatusFilter(admin.SimpleListFilter):
    title = 'Active Status'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Yes'),
            ('no', 'No'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(is_active=True)
        if self.value() == 'no':
            return queryset.filter(is_active=False)








# Register your custom filters and UserAdmin class



# # You can also add UserProfile fields as inline if needed
# class UserProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'User Profiles'

# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'phone_number', 'profile_image')



# Register your models here.
admin.site.register(Profile)



@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patientID', 'firstName', 'lastName', 'email', 'phoneNo', 'sex')

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('predictionID', 'patientID', 'predictionDate', 'result')

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('userRoleID', 'userID', 'roleID')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('userID', 'firstName', 'lastName', 'email', 'phoneNo', 'sex', 'is_active', 'is_staff', 'is_superuser')

class UserAdmin(BaseUserAdmin):
    list_display = ('userID', 'firstName', 'lastName', 'email', 'phoneNo', 'sex', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('userID', 'firstName', 'lastName', 'email')
    list_editable = ('is_active', 'is_staff', 'is_superuser')
    actions = ["make_active", "make_inactive"]  # Ensure "change_user" is not removed

class CustomUserAdmin(BaseUserAdmin):
    list_display = ('userID', 'firstName', 'lastName', 'email', 'phoneNo', 'sex', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('userID', 'firstName', 'lastName', 'email')
    list_editable = ('is_active', 'is_staff', 'is_superuser')

    def edit_selected_users(self, request, queryset):
        # Redirect to the edit page for the first selected user (assuming only one is selected)
        if queryset.count() == 1:
            user = queryset.first()
            return HttpResponseRedirect(reverse('admin:auth_user_change', args=[user.id]))
    edit_selected_users.short_description = "Edit Selected Users"

    actions = [edit_selected_users]


@admin.register(DoctorPatientRel)
class DoctorPatientRelAdmin(admin.ModelAdmin):
    list_display = ('relationID', 'userID', 'patientID', 'startDate', 'endDate')

@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('planID', 'patientID', 'doctorID', 'planDate', 'content')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('roleID', 'roleName', 'Desc')

@admin.register(PatientDetails)
class PatientDetailsAdmin(admin.ModelAdmin):
    list_display = ('detailsID', 'patientID', 'dob', 'cp', 'trestbps', 'chol', 'fps', 'restech', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal', 'target', 'date')

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reportID', 'reportTitle', 'userID', 'predictionID', 'detailsID', 'generatedDate')

    from django.contrib.auth.models import User, Group

    admin.site.unregister(Group)
    # admin.site.unregister(User)
    