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
    path('profile/<user_id>', views.showStaff, name='showStaff'),
    path('addPatient/', views.addPatient, name='addPatient'),


]