from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile_list/', views.profile_list, name='profile_list'),
    path('login/', views.login_user, name='login')
    # path('logout/', views.logout_user, name='logout'),

]