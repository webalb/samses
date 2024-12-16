from django.urls import path
from schools.views import views, classroom_create

app_name = 'schools'

urlpatterns = [
    
    path('', views.school_list, name='list'),
    path('create/', views.school_create, name='create'),
    path('<uuid:pk>/details/', views.school_details, name='details'),
    path('<uuid:pk>/update/', views.school_update, name='update'),
    path('<uuid:pk>/confirm_delete/', views.school_delete, name='delete'),

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
    path('subjects/<int:pk>/update/', views.subject_update, name='subject_update'),
    path('subjects/<int:pk>/delete/', views.subject_delete, name='subject_delete'),

    path('stakeholders/<uuid:pk>/create/', views.stakeholder_create, name='stakeholder_create'),
    path('stakeholders/<int:pk>/update/', views.stakeholder_update, name='stakeholder_update'),
    path('stakeholders/<int:pk>/delete/', views.stakeholder_delete, name='stakeholder_delete'),

    path('metadata/<uuid:pk>/set/', views.metadata_set, name='metadata_set'),
    path('metadata/<int:pk>/update/', views.metadata_update, name='metadata_update'),
    path('metadata/<int:pk>/delete/', views.metadata_delete, name='metadata_delete'),

    path('accreditation/<uuid:pk>/set/', views.accreditation_set, name='accreditation_set'),
    path('accreditation/<int:pk>/update/', views.accreditation_update, name='accreditation_update'),
    path('accreditation/<int:pk>/delete/', views.accreditation_delete, name='accreditation_delete'),

    path('suspension-closure/<uuid:pk>/set/', views.suspension_set, name='suspension_set'),
    path('suspension-closure/<int:pk>/update/', views.suspension_update, name='suspension_update'),
    path('suspension-closure/<int:pk>/drop/', views.suspension_drop, name='suspension_drop'),
    
    path('inspection-report/<uuid:pk>/set/', views.inspection_report_set, name='inspection_report_set'),
    path('inspection-report/<int:pk>/update/', views.inspection_report_update, name='inspection_report_update'),
    path('inspection-report/<int:pk>/delete/', views.inspection_report_delete, name='inspection_report_delete'),

    path('classrooms/<uuid:school_id>/create/', classroom_create, name='classroom_create'),
    # path('library/<uuid:school_id>/create/', views.library_create, name='library_create'),
    # path('laboratory/<uuid:school_id>/create/', views.laboratory_create, name='laboratory_create'),
    # path('computer-lab/<uuid:school_id>/create/', views.computer_lab_create, name='computer_lab_create'),
    # path('sports-facility/<uuid:school_id>/create/', views.sports_facility_create, name='sports_facility_create'),
]
