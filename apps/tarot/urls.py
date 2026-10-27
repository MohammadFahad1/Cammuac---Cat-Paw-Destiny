from django.urls import path
from . import views

urlpatterns = [
    path('today/', views.TodayCatTarotAPIView.as_view(), name='cat-tarot-today-alias'),
]

