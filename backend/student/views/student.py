from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.views.generic import DetailView


from backend.student.forms import StudentForm
from backend.student.models import Student

class StudentListView(View):
    """
    Displays a list of all students.
    """
    template_name = "student/student_list.html"

    def get(self, request):
        students = Student.objects.all()
        context = {"students": students,}
        return render(request, self.template_name, context)

class StudentDetailView(DetailView):
    model = Student
    template_name = "student/student_details.html"

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        subjects = get_student_subjects(student)
        context = {'student': student, 'subjects': subjects}
        return render(request, self.template_name, context)


from django.db.models import Q
from backend.schools.models import SubjectRepository
def get_student_subjects(student):
    """
    Fetch all subjects for a student based on their class (program_level) and stream.
    """
    program_level = student.enrollment_record.program_level
    stream = student.enrollment_record.stream
    school = student.school

    subjects = SubjectRepository.objects.filter(
        Q(program_levels=program_level.program_level_template)
        & (
            Q(streams=stream)  # If stream is applicable
            | Q(streams__isnull=True)  # Or if no stream is set for the subject
        )
    ).filter(
        Q(school_subjects__school=school) | Q(school_subjects__school__isnull=True)
    ).distinct()

    return subjects

class StudentCreateView(View):
    """
    Handles the creation of a new student record.
    """
    template_name = "student/form.html"
    success_url = reverse_lazy("student:list")

    def get(self, request):
        form = StudentForm()
        return render(request, self.template_name, {"form": form, "obj_name": "Add Student"})

    def post(self, request):
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Student record created successfully.")
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form, "obj_name": "Add Student"})


class StudentUpdateView(View):
    """
    Handles updating an existing student record.
    """
    template_name = "student/form.html"
    success_url = reverse_lazy("student:list")

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student)
        return render(request, self.template_name, {"form": form, "obj_name": "Update Student", "student": student})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student record updated successfully.")
            return redirect(self.success_url)
        return render(request, self.template_name, {"form": form, "obj_name": "Update Student", "student": student})


class StudentDeleteView(View):
    """
    Handles deleting a student record.
    """
    template_name = "student/confirm_delete.html"
    success_url = reverse_lazy("student:list")

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, self.template_name, {"object": student})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        messages.success(request, "Student record deleted successfully.")
        return redirect(self.success_url)
