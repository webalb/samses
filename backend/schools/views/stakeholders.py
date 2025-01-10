from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from backend.schools.models import Staff, School
from backend.schools.forms import StaffForm

# Create Staff
def staff_create(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            staff = form.save(commit=False)
            staff.school = school
            staff.save()
            messages.success(request, f"Staff member {staff.full_name} has been added.")
            return redirect('schools:details', pk=school.id)
    else:
        form = StaffForm()
    return render(request, 'schools/create.html', {'form': form, 'object': school, 'obj_name': 'Staff'})

# Update Staff
def staff_update(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            messages.success(request, f"Staff member {staff.full_name} has been updated.")
            return redirect('schools:details', pk=staff.school.id)
    else:
        form = StaffForm(instance=staff)
    return render(request, 'schools/create.html', {'form': form, 'object': staff, 'obj_name': 'Staff'})

# Delete Staff
def staff_delete(request, pk):
    staff = get_object_or_404(Staff, pk=pk)
    school = staff.school
    if request.method == 'POST':
        staff.delete()
        messages.success(request, f"Staff member {staff.full_name} has been removed.")
        return redirect('schools:details', pk=school.id)
    return render(request, 'schools/confirm_delete.html', {'object': staff, 'school': school, 'obj_name': 'Staff'})
