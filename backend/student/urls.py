from django.urls import path
from backend.student.views import (
    student,
    guardian,
    academic,
)
app_name = 'student'
urlpatterns = [
    path('', student.StudentListView.as_view(), name='list'),
    path('create/', student.StudentCreateView.as_view(), name='create'),
    path('<uuid:pk>/update/', student.StudentUpdateView.as_view(), name='update'),
    path('<uuid:pk>/delete/', student.StudentDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/details/', student.StudentDetailView.as_view(), name='details'),

    path('guardian/<uuid:student_id>/create/', guardian.AddGuardianView.as_view(), name='guardian_create'),
    path('guardian/<int:guardian_id>/edit/', guardian.UpdateGuardianView.as_view(), name='guardian_update'),
    path('guardian/<int:guardian_id>/delete/', guardian.DeleteGuardianView.as_view(), name='guardian_delete'),

    path('<uuid:student_id>/select-school/', academic.select_school_view, name='select_school'),
    path('<uuid:student_id>/<uuid:school_id>/set-program/', academic.set_program_view, name='set_program'),
    path('<uuid:student_id>/<uuid:school_id>/<str:program>/set-program-level/', academic.set_program_level_stream_view, name='set_program_level'),
    path('<uuid:student_id>/<uuid:school_id>/<int:program_level_id>/finalize-enrollment/', academic.enrollment_final_view, name='enrollment_final_no_stream'),
    path('<uuid:student_id>/<uuid:school_id>/<int:program_level_id>/<int:stream_id>/finalize-enrollment/', academic.enrollment_final_view, name='enrollment_final'),

    path('enrollment/<int:pk>/update/', academic.EnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollment/<int:pk>/delete/', academic.EnrollmentDeleteView.as_view(), name='enrollment_delete'),

    path('admission-letter/<int:enrollment_id>/', academic.viewAdmissionLetter, name='admission_letter'),

]
