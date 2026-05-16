from django.urls import path
from . import views

app_name = 'timesheet'

urlpatterns = [
    path('', views.timesheet_view, name='index'),
    path('api/save/', views.save_time_entry, name='api_save'),
]