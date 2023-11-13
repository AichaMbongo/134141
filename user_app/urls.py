from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    
    path('profile_list/', views.profile_list, name='profile_list'),
    path('profile/<int:pk>', views.profile, name='profile'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('Patient/', views.listPatient, name='listPatient'),
    path('showPatient/<patient_id>', views.showPatient, name='showPatient'),
    path('addPatientDetails/<patient_id>', views.addPatientDetails, name='addPatientDetails'),
    path('profile/<user_id>', views.showStaff, name='showStaff'),
    path('addPatient/', views.addPatient, name='addPatient'),
    path('updateUser/', views.updateUser, name='updateUser'),
    path('updatePatientDetails/<int:patient_id>/', views.updatePatientDetails, name='updatePatientDetails'),
    path('confirmTreatment/<int:patient_id>/', views.ConfirmTreatment, name='confirmTreatment'),
    path('treatment_plan/<int:patient_id>/', views.treatment_plan, name='treatment_plan'),
    path('patientPrediction/<int:patient_id>/', views.patientPrediction, name='patientPrediction'),
    path('make_appointment/<int:patient_id>/', views.make_appointment, name='make_appointment'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('view_assigned_patients/', views.view_assigned_patients, name='view_assigned_patients'),
    path('view_health_records/<int:patient_id>/', views.view_health_records, name='view_health_records'),
    path('predict_health_records/<int:patient_id>/', views.predict_health_records, name='predict_health_records'),
    path('fill_patient_details/<int:patient_id>/', views.fill_patient_details, name='fill_patient_details'),
    path('index/', views.index, name='index'),
    path('result_pdf/', views.result_pdf, name='result_pdf'),
    path('users_csv/', views.users_csv, name='users_csv'),
    path('appointment_csv/', views.appointment_csv, name='appointment_csv'),
    path('heart_disease_prediction//<int:patient_id>/', views.heart_disease_prediction, name='heart_disease_prediction'),

    # path('confirm-conclusion/<int:patient_id>/', views.ConfirmConclusion, name='confirmConclusion'),
    

]