from django.urls import path
from . import views

urlpatterns = [
    path('user_app/', views.user_app, name='user_app'),
]