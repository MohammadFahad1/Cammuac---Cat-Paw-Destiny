from django.urls import path
from . import views

urlpatterns = [
    path('', views.LetterListCreateAPIView.as_view(), name='letter-list-create'),
    path('<int:pk>/', views.LetterDetailAPIView.as_view(), name='letter-detail'),
]

