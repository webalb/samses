from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.exceptions import ValidationError

from .forms import StudentForm
from .models import Student

class StudentCreateView(View):
    def get(self, request):
        form = StudentForm()
        return render(request, 'students/student_create.html', {'form': form})

    def post(self, request):
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('students:list')  # Change to your success URL
            except ValidationError as e:
                form.add_error(None, e)
        return render(request, 'students/student_create.html', {'form': form})


class StudentListView(View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'students/student_list.html', {'students': students})

class StudentDetailView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, 'students/student_details.html', {'student': student})

class StudentUpdateView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(instance=student)
        return render(request, 'students/student_create.html', {'form': form, 'student': student})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            return redirect('students:list')  # Change to your success URL
        return render(request, 'students/student_create.html', {'form': form, 'student': student})

class StudentDeleteView(View):
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        return render(request, 'students/student_confirm_delete.html', {'student': student})

    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        student.delete()
        return redirect('students:list')  # Change to your success URL
