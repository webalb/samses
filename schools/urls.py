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

    path('stakeholders/<int:pk>/create/', views.stakeholder_create, name='stakeholder_create'),
    path('stakeholders/<int:pk>/update/', views.stakeholder_update, name='stakeholder_update'),
    path('stakeholders/<int:pk>/delete/', views.stakeholder_delete, name='stakeholder_delete'),

    path('metadata/<int:pk>/set/', views.metadata_set, name='metadata_set'),
    path('metadata/<int:pk>/update/', views.metadata_update, name='metadata_update'),
    path('metadata/<int:pk>/delete/', views.metadata_delete, name='metadata_delete'),

    path('accreditation/<int:pk>/set/', views.accreditation_set, name='accreditation_set'),
    path('accreditation/<int:pk>/update/', views.accreditation_update, name='accreditation_update'),
    path('accreditation/<int:pk>/delete/', views.accreditation_delete, name='accreditation_delete'),

    path('suspension-closure/<int:pk>/set/', views.suspension_set, name='suspension_set'),
    path('suspension-closure/<int:pk>/update/', views.suspension_update, name='suspension_update'),
    path('suspension-closure/<int:pk>/delete/', views.suspension_delete, name='suspension_delete'),
    
    path('inspection-report/<int:pk>/set/', views.inspection_report_set, name='inspection_report_set'),
    path('inspection-report/<int:pk>/update/', views.inspection_report_update, name='inspection_report_update'),
    path('inspection-report/<int:pk>/delete/', views.inspection_report_delete, name='inspection_report_delete'),

]

