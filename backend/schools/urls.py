from django.urls import path
from backend.schools.views import (
    views,
    infrastructure_views,
    complete_current_sessions,
    complete_session,
    vocational,
    level,
    feedback,
    grading,
    stakeholders,
    finance,
)
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
    
    path("complete-sessions/", complete_current_sessions, name="complete_current_sessions"),
    path("complete-session/<int:session_id>/", complete_session, name="complete_session"),

    path('terms/<int:pk>/', views.term_detail, name='term_detail'),
    path('terms/<int:academic_session_id>/create/', views.term_create, name='term_create'),
    path('terms/<int:pk>/update/', views.term_update, name='term_update'),
    path('terms/<int:pk>/delete/', views.term_delete, name='term_delete'),


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
    path('inspection-report/<uuid:school_id>/all/', views.inspection_report_all, name='inspection_report_all'),

    path('classrooms/<uuid:school_id>/create/', infrastructure_views.classroom_create, name='classroom_create'),
    path('classrooms/<uuid:school_id>/update/', infrastructure_views.classroom_update, name='classroom_update'),
    path('classrooms/<uuid:school_id>/delete/', infrastructure_views.classroom_delete, name='classroom_delete'),
    
    path('library/<uuid:school_id>/create/', infrastructure_views.library_create, name='library_create'),
    path('library/<uuid:school_id>/update/', infrastructure_views.library_update, name='library_update'),
    path('library/<uuid:school_id>/delete/', infrastructure_views.library_delete, name='library_delete'),
    
    path('laboratory/<uuid:school_id>/create/', infrastructure_views.laboratory_create, name='laboratory_create'),
    path('laboratory/<uuid:school_id>/update/', infrastructure_views.laboratory_update, name='laboratory_update'),
    path('laboratory/<uuid:school_id>/delete/', infrastructure_views.laboratory_delete, name='laboratory_delete'),

    path('computer-lab/<uuid:school_id>/create/', infrastructure_views.computer_lab_create, name='computer_lab_create'),
    path('computer-lab/<uuid:school_id>/update/', infrastructure_views.computer_lab_update, name='computer_lab_update'),
    path('computer-lab/<uuid:school_id>/delete/', infrastructure_views.computer_lab_delete, name='computer_lab_delete'),

    path('sports-facility/<uuid:school_id>/create/', infrastructure_views.sports_facility_create, name='sports_facility_create'),
    path('sports-facility/<uuid:school_id>/update/', infrastructure_views.sports_facility_update, name='sports_facility_update'),
    path('sports-facility/<uuid:school_id>/delete/', infrastructure_views.sports_facility_delete, name='sports_facility_delete'),
    
    path('special-needs/<uuid:school_id>/create/', infrastructure_views.special_needs_create, name='special_needs_create'),
    path('special-needs/<uuid:school_id>/update/', infrastructure_views.special_needs_update, name='special_needs_update'),
    path('special-needs/<uuid:school_id>/delete/', infrastructure_views.special_needs_delete, name='special_needs_delete'),

    path('vocational-departments/', vocational.vocational_department_list, name='department_list'),
    path('vocational-departments/create/', vocational.vocational_department_create, name='vocational_department_create'),
    path('vocational-departments/<int:department_id>/update/', vocational.vocational_department_update, name='vocational_department_update'),
    path('vocational-departments/<int:department_id>/delete/', vocational.vocational_department_delete, name='vocational_department_delete'),
    
    path('vocational-departments/<uuid:school_id>/create/', vocational.school_department_create, name='school_department_create'),
    path('school-vocational-departments/<int:pk>/update/', vocational.school_department_update, name='school_department_update'),
    path('school-vocational-departments/<int:pk>/delete/', vocational.school_department_delete, name='school_department_delete'),
    path('<uuid:school_id>/departments/add_all/', vocational.school_department_add_all, name='school_department_add_all'),

    path('vocational-partnerships/<uuid:school_id>/create/', vocational.vocational_partnership_create, name='vocational_partnership_create'),
    path('vocational-partnerships/<int:pk>/update/', vocational.vocational_partnership_update, name='vocational_partnership_update'),
    path('vocational-partnerships/<int:pk>/delete/', vocational.vocational_partnership_delete, name='vocational_partnership_delete'),

    path('level-classes/<uuid:school_id>/create/', level.level_class_create, name='level_classes_create'),
    path('level-classes/<int:pk>/update/', level.level_class_update, name='level_classes_update'),
    path('level-classes/<int:pk>/delete/', level.level_class_delete, name='level_classes_delete'),

    path('level-classes/<int:level_class_id>/add-class/', level.level_classes_create_for_existing, name='level_classes_create_for_existing'),
    path('level-classes/<uuid:school_id>/program-level/<int:program_level_id>/add-class/', level.level_classes_create, name='level_classes_create'),
    path('class/<int:pk>/details', level.class_detail_view, name='class_detail'),

    path('subject/create/', level.subject_create, name='subject_create'),
    path('subject/<int:pk>/update/', level.subject_update, name='subject_update'),
    path('subject/<int:pk>/delete/', level.subject_delete, name='subject_delete'),
    path('subjects/', level.subject_list, name='subject_list'),
    path('subjects/<int:pk>/detail/', level.subject_detail, name='subject_detail'),

    path('<uuid:school_id>/subjects/', level.school_subject_list, name='school_subject_list'),
    path('<uuid:school_id>/subjects/create/', level.school_subject_create, name='school_subject_create'),
    path('subjects/<int:pk>/update/for-school', level.school_subject_update, name='school_subject_update'),
    path('subjects/<int:pk>/delete/for-school', level.school_subject_delete, name='school_subject_delete'),
    path('<uuid:school_id>/subjects/add_all/', level.school_subject_add_all, name='school_subject_add_all'),

    path('<uuid:school_id>/feedbacks/create/', feedback.feedback_create, name='feedback_create'),
    path('feedbacks/<int:feedback_id>/', feedback.feedback_detail, name='feedback_detail'),
    path('feedbacks/<int:feedback_id>/delete/', feedback.feedback_delete, name='feedback_delete'),

    path('grading-scales/create/', grading.grading_scale_create, name='grading_scale_create'),
    path('grading-scales/<int:pk>/update/', grading.grading_scale_update, name='grading_scale_update'),
    path('grading-scales/<int:pk>/delete/', grading.grading_scale_delete, name='grading_scale_delete'),
    path('grading-scales/<int:pk>/detail/', grading.grading_scale_detail, name='grading_scale_detail'),

    path('grading-scales/<int:grading_scale_id>/grade-boundaries/create/', grading.grade_boundary_create, name='grade_boundary_create'),
    path('grade-boundaries/<int:pk>/update/', grading.grade_boundary_update, name='grade_boundary_update'),
    path('grade-boundaries/<int:pk>/delete/', grading.grade_boundary_delete, name='grade_boundary_delete'),

    path('subjects/<int:subject_id>/grading-configurations/create/', grading.subject_grading_create, name='subject_grading_create'),
    path('grading-configurations/<int:pk>/update/', grading.subject_grading_update, name='subject_grading_update'),
    path('grading-configurations/<int:pk>/delete/', grading.subject_grading_delete, name='subject_grading_delete'),
    path("subjects/configure-grading-scale/for-all", grading.configure_grading_scales_all, name="configure_grading_scales_all"),
    
    path("<uuid:pk>/parent-engagements/create/", views.parent_engagement_create, name="parent_engagement_create"),
    path("parent-engagements/<int:pk>/update/", views.parent_engagement_update, name="parent_engagement_update"),
    path("parent-engagements/<int:pk>/delete/", views.parent_engagement_delete, name="parent_engagement_delete"),

    path('staff/<uuid:school_id>/create/', stakeholders.staff_create, name='staff_create'),
    path('staff/<int:pk>/update/', stakeholders.staff_update, name='staff_update'),
    path('staff/<int:pk>/delete/', stakeholders.staff_delete, name='staff_delete'),

    path('finance/<uuid:school_id>/details/', finance.school_finance, name='school_finance'),
    
    path('fee-structure/<uuid:school_id>/create/', finance.fee_structure_create, name='fee_structure_create'),
    path('fee-structure/<int:pk>/update/', finance.fee_structure_update, name='fee_structure_update'),
    path('fee-structure/<int:pk>/delete/', finance.fee_structure_delete, name='fee_structure_delete'),

    path('<uuid:school_id>/attendance-settings/', views.attendance_settings_view, name='attendance_settings'),

]
