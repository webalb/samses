from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from backend.student.forms import SelectSchoolForm, SetProgramForm, SetProgramLevelStreamForm, EnrollmentFinalForm
from backend.schools.models import School, LevelClasses, Stream
from backend.student.models import EnrollmentRecord, Student

def select_school_view(request, student_id):
    """
    Step 1: Select a school for the student.
    """
    student = get_object_or_404(Student, pk=student_id)

    if request.method == 'POST':
        form = SelectSchoolForm(request.POST)
        if form.is_valid():
            school = form.cleaned_data['school']
            return redirect(reverse('student:set_program', kwargs={'student_id': student.id, 'school_id': school.id}))
    else:
        form = SelectSchoolForm()

    return render(request, 'student/enrollment_forms/select_school.html', {'form': form, 'student': student})

def set_program_view(request, student_id, school_id):
    """
    Step 2: Set the program offered by the school.
    """
    student = get_object_or_404(Student, pk=student_id)
    school = get_object_or_404(School, pk=school_id)

    if request.method == 'POST':
        form = SetProgramForm(request.POST, school=school)
        if form.is_valid():
            program = form.cleaned_data['program']
            return redirect(reverse('student:set_program_level', kwargs={
                'student_id': student.id, 'school_id': school.id, 'program': program
            }))
    else:
        form = SetProgramForm(school=school)

    return render(request, 'student/enrollment_forms/set_program.html', {'form': form, 'school': school, 'student': student})


def set_program_level_stream_view(request, student_id, school_id, program):
    """
    Step 3: Set program level and stream for the student.
    """
    student = get_object_or_404(Student, pk=student_id)
    school = get_object_or_404(School, pk=school_id)

    if request.method == 'POST':
        form = SetProgramLevelStreamForm(request.POST, school=school, program=program)
        if form.is_valid():
            program_level_id = form.cleaned_data['program_level']
            program_level = get_object_or_404(LevelClasses, pk=program_level_id)if program_level_id else None
            stream_id = form.cleaned_data.get('stream')
            stream = get_object_or_404(Stream, pk=stream_id) if stream_id else None
            if stream:
                return redirect(reverse('student:enrollment_final', kwargs={
                    'student_id': student.id, 'school_id': school.id,
                    'program_level_id': program_level.id, 'stream_id': stream.id if stream else None
                }))
            return redirect(reverse('student:enrollment_final_no_stream', kwargs={
                    'student_id': student.id, 'school_id': school.id,
                    'program_level_id': program_level.id
                }))
    else:
        form = SetProgramLevelStreamForm(school=school, program=program)

    return render(request, 'student/enrollment_forms/set_program_level.html', {'form': form, 'school': school, 'program': program, 'student': student})

def enrollment_final_view(request, student_id, school_id, program_level_id, stream_id=None):
    """
    Step 4: Finalize the enrollment.
    """
    student = get_object_or_404(Student, pk=student_id)
    school = get_object_or_404(School, pk=school_id)
    program_level = get_object_or_404(LevelClasses, pk=program_level_id)
    stream = get_object_or_404(Stream, pk=stream_id) if stream_id else None

    if request.method == 'POST':
        form = EnrollmentFinalForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student
            enrollment.school = school
            
            student.school = school
            student.save()

            enrollment.program_level = program_level
            enrollment.program = program_level.program_level_template.program
            enrollment.stream = stream
            enrollment.academic_session = school.get_academic_session()
            enrollment.save()
            messages.success(request, "Enrollment information set successfully for this student.")
            return redirect('student:details', pk=student.pk)
    else:
        form = EnrollmentFinalForm()

    return render(request, 'student/enrollment_forms/enrollment_final.html', {
        'form': form, 'student': student, 'school': school, 'program_level': program_level, 'stream': stream
    })

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import UpdateView, DeleteView
from backend.student.models import EnrollmentRecord
from backend.student.forms import EnrollmentRecordForm

class EnrollmentUpdateView(View):
    """
    Handles GET and POST requests to update an EnrollmentRecord.
    """
    template_name = "student/form.html"

    def get(self, request, pk):
        enrollment = get_object_or_404(EnrollmentRecord, pk=pk)
        form = EnrollmentRecordForm(instance=enrollment)
        return render(request, self.template_name, {
            'form': form,
            'object': enrollment.student,
            'obj_name': "Student Enrollment Record",
        })

    def post(self, request, pk):
        enrollment = get_object_or_404(EnrollmentRecord, pk=pk)
        form = EnrollmentRecordForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            return redirect('student:details', pk=enrollment.student.pk)
        return render(request, self.template_name, {
            'form': form,
            'object': enrollment.student,
            'obj_name': "Student Enrollment Record",
        })

class EnrollmentDeleteView(DeleteView):
    """
    Handles deletion of an EnrollmentRecord.
    """
    model = EnrollmentRecord
    template_name = "student/confirm_delete.html"
    context_object_name = "object"

    def get_success_url(self):
        # Redirect to the student's details page
        return reverse_lazy('student:details', kwargs={'pk': self.object.student.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['obj_name'] = "Student Enrollment Information"
        return context
# #10600c - green color for samses logo. #a6a6a6 secondary color


def viewAdmissionLetter(request, enrollment_id):
    try:
        enrollment = EnrollmentRecord.objects.get(pk=enrollment_id)

    except EnrollmentRecord.DoesNotExist:
        return HttpResponse("Enrollment not found.", status=404)
    context = {'enrollment': enrollment, 'school': enrollment.school, 'student': enrollment.student}
    return render(request, 'student/printable/admission_letter.html', context)
