from django.urls import path
from . import views

urlpatterns = [
    path('daily-check-in/today/', views.TodayCheckInAPIView.as_view(), name='today-check-in'),
]
