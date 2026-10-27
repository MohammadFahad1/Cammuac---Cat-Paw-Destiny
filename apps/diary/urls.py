from django.urls import path
from . import views

urlpatterns = [
    path('', views.DiaryNoteListCreateAPIView.as_view(), name='diary-list-create'),
    path('<int:pk>/', views.DiaryNoteDetailAPIView.as_view(), name='diary-detail'),
]

