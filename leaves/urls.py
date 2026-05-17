from django.urls import path
from . import views

app_name = 'leaves'

urlpatterns = [
    path('', views.LeaveListView.as_view(), name='list'),
    path('create/', views.LeaveCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.LeaveUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.LeaveDeleteView.as_view(), name='delete'),
    path('api/check-collision/', views.api_check_ts_collision, name='check_collision'),
]
