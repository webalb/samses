from django.urls import path
from .views import (
    StudentCreateView, StudentListView, StudentUpdateView, StudentDeleteView, 
    StudentDetailView,
)
app_name = 'students'
urlpatterns = [
    path('', StudentListView.as_view(), name='list'),
    path('create/', StudentCreateView.as_view(), name='create'),
    path('<int:pk>/update', StudentUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', StudentDeleteView.as_view(), name='delete'),
    path('<int:pk>/details/', StudentDetailView.as_view(), name='details'),
    # Add other URL patterns here
]
