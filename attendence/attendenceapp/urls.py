from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recognize/', views.recognize, name='recognize'),
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/download/', views.download_attendance_pdf, name='download_attendance_pdf'),
]