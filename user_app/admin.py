from django.contrib import admin
from .models import Patient, Prediction, UserRole, User, DoctorPatientRel, TreatmentPlan, Role, PatientDetails, Report

# Register your models here.

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
    list_display = ('userID', 'firstName', 'lastName', 'email', 'phoneNo', 'sex')

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