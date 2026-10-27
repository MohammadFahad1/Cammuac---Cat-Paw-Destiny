from django.urls import path
from . import views

urlpatterns = [
    path('today/', views.TodayCheckInAPIView.as_view(), name='today-check-in'),
    path('alarms/', views.AlarmListCreateAPIView.as_view(), name='alarm-list-create'),
    path('alarms/<int:pk>/', views.AlarmDetailAPIView.as_view(), name='alarm-detail'),
]
