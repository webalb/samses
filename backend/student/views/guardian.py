from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from backend.student.models import Student, Guardian
from backend.student.forms import GuardianForm


class AddGuardianView(View):

    template_name = 'student/form.html'

    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        form = GuardianForm()
        return render(request, self.template_name, {'form': form, 'object': student, 'obj_name': 'Student guardians'})

    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        form = GuardianForm(request.POST)
        if form.is_valid():
            guardian = form.save(commit=False)
            guardian.student = student
            guardian.save()
            messages.success(request, f"Guardian added successfully for {student.full_name}.")
            return redirect(student.get_absolute_url())
        return render(request, self.template_name, {'form': form, 'object': student, 'obj_name': 'Student guardians'})

class UpdateGuardianView(View):

    template_name = 'student/form.html'

    def get(self, request, guardian_id):
        guardian = get_object_or_404(Guardian, pk=guardian_id)
        form = GuardianForm(instance=guardian)
        return render(request, self.template_name, {'form': form, 'object': guardian, 'obj_name': 'Student guardians'})

    def post(self, request, guardian_id):
        guardian = get_object_or_404(Guardian, pk=guardian_id)
        form = GuardianForm(request.POST, instance=guardian)
        if form.is_valid():
            form.save()
            messages.success(request, "Guardian information updated successfully.")
            return redirect(guardian.student.get_absolute_url())
        return render(request, self.template_name, {'form': form, 'object': guardian, 'obj_name': 'Student guardians'})

class DeleteGuardianView(View):

    template_name = 'student/confirm_delete.html'
    def get(self, request, guardian_id):
        guardian = get_object_or_404(Guardian, pk=guardian_id)
        return render(request, self.template_name, {'object': guardian, 'obj_name': 'Student guardians'})

    def post(self, request, guardian_id):
        guardian = get_object_or_404(Guardian, pk=guardian_id)
        student = guardian.student
        guardian.delete()
        messages.success(request, "Guardian deleted successfully.")
        return redirect(student.get_absolute_url())
