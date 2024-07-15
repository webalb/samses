from django.urls import path
from . import views

app_name = 'schools'

urlpatterns = [
    
    path('', views.school_list, name='list'),
    path('create/', views.school_create, name='create'),
    path('<int:pk>/details/', views.school_details, name='details'),
    path('<int:pk>/update/', views.school_update, name='update'),
    path('<int:pk>/confirm_delete/', views.school_delete, name='delete'),

    path('academic_sessions', views.academic_session_list, name='academic_sessions'),
    path('academic_session_create/', views.academic_session_create, name='academic_session_create'),
    path('academic_session/<int:pk>/update/', views.academic_session_update, name='academic_session_update'),
    path('academic_session/<int:pk>/confirm_delete/', views.academic_session_delete, name='academic_session_delete'),
   
    path('terms/', views.term_list, name='term_list'),
    path('terms/<int:pk>/', views.term_detail, name='term_detail'),
    path('terms/<int:academic_session_id>/set_or_update/', views.term_create_or_update, name='term_create_or_update'),
    path('terms/<int:academic_session_id>/delete/', views.term_delete, name='term_delete'),

    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_create, name='subject_create'),
]

