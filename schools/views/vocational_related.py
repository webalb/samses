from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from schools.forms import VocationalPartnershipForm, DepartmentRepositoryForm, SchoolDepartmentForm
from schools.models import DepartmentRepository, School, VocationalPartnership, SchoolDepartment


def vocational_department_create(request):
    if request.method == 'POST':
        form = DepartmentRepositoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department added successfully!')
            return redirect('schools:department_list')
    else:
        form = DepartmentRepositoryForm()
    
    return render(request, 'schools/vocational_department_create.html', {'form': form, 'obj_name': 'Vocational Department'})


def vocational_department_list(request):
    departments = DepartmentRepository.objects.all()
    return render(request, 'schools/vocational_department_list.html', {'departments': departments})


def vocational_department_update(request, department_id):
    department = get_object_or_404(DepartmentRepository, pk=department_id)

    if request.method == 'POST':
        form = DepartmentRepositoryForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, 'Department updated successfully!')
            return redirect('schools:department_list')
    else:
        form = DepartmentRepositoryForm(instance=department)
    
    return render(request, 'schools/vocational_department_create.html', {'form': form, 'object': department})

def vocational_department_delete(request, department_id):
    department = get_object_or_404(DepartmentRepository, pk=department_id)
    if request.method == 'POST':
        department.delete()
        messages.success(request, "Vocational Department deleted successfully!")
        return redirect('schools:department_list')
    return render(request, 'schools/confirm_delete.html', {'object': department,'obj_name': 'Vocational department'})

# ==================================
# ||| SCHOOL DEPARTMENTS/PROGRAMS|||
# ==================================

def school_department_create(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    if request.method == 'POST':
        form = SchoolDepartmentForm(request.POST)
        if form.is_valid():
            school_department = form.save(commit=False)
            school_department.school = school
            school_department.save()
            messages.success(request, 'School department added successfully!')
            return redirect('schools:details', pk=school.pk)
    else:
        form = SchoolDepartmentForm(school=school)

    return render(request, 'schools/create.html', {'form': form, 'obj_name': 'School departments', 'object': school})

# Add All Subjects to School Confirmation View
def school_department_add_all(request, school_id):
    school = get_object_or_404(School, pk=school_id)

    # Split the school's program into components (e.g., 'jss+sss' -> ['jss', 'sss'])
    program_components = school.program.split('+')

    # Get all subjects from the SubjectRepository that match the school's program levels
    all_departments = DepartmentRepository.objects.all().exclude(
        id__in=school.school_departments.values_list('departments', flat=True)
    ).distinct()

    if request.method == 'POST':
        # Add all the remaining subjects to the school
        for departments in all_departments:
            school.school_departments.create(departments=departments)
        messages.success(request, 'All departments added successfully!')
        return redirect('schools:details', school.pk)  # Redirect to the list page after adding subjects

    return render(request, 'schools/school_department_add_all.html', {
        'school': school,
        'all_departments': all_departments,
    })

def school_department_update(request, pk):
    school_department = get_object_or_404(SchoolDepartment, pk=pk)
    if request.method == 'POST':
        form = SchoolDepartmentForm(request.POST, instance=school_department)
        if form.is_valid():
            form.save()
            messages.success(request, 'School department updated successfully!')
            return redirect('schools:details', pk=school_department.school.pk)
    else:
        form = SchoolDepartmentForm(instance=school_department, school=school_department.school)
    departments = DepartmentRepository.objects.all()
    return render(request, 'schools/create.html', {'form': form, 'object': school_department, 'obj_name': 'School department'})

def school_department_delete(request, pk):
    school_department = get_object_or_404(SchoolDepartment, pk=pk)
    if request.method == 'POST':
        school_department.delete()
        messages.success(request, 'School department updated successfully!')
        return redirect('schools:details', pk=school_department.school.pk)
    return render(request, 'schools/confirm_delete.html', {'object': school_department, 'obj_name': 'School department'})
# =============================
# ||| VOCATIONAL PARTNERSHIP|||
# =============================
def vocational_partnership_create(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    if request.method == 'POST':
        form = VocationalPartnershipForm(request.POST)
        if form.is_valid():
            partnership = form.save(commit=False)
            partnership.school = school
            partnership.save()
            messages.success(request, "Vocational Partnership added successfully!")
            return redirect('schools:details', pk=school.id)
    else:
        form = VocationalPartnershipForm()
    return render(request, 'schools/create.html', {'form': form, 'object': school, 'obj_name': 'Vocational partnership'})

def vocational_partnership_update(request, pk):
    partnership = get_object_or_404(VocationalPartnership, pk=pk)
    if request.method == 'POST':
        form = VocationalPartnershipForm(request.POST, instance=partnership)
        if form.is_valid():
            form.save()
            messages.success(request, "Vocational Partnership updated successfully!")
            return redirect('schools:details', pk=partnership.school.id)
    else:
        form = VocationalPartnershipForm(instance=partnership)
    return render(request, 'schools/create.html', {'form': form, 'object': partnership, 'obj_name': 'Vocational partnership'})

def vocational_partnership_delete(request, pk):
    partnership = get_object_or_404(VocationalPartnership, pk=pk)
    if request.method == 'POST':
        school_id = partnership.school.id  # Save school ID for redirection
        partnership.delete()
        messages.success(request, "Vocational Partnership deleted successfully!")
        return redirect('schools:details', pk=school_id)
    return render(request, 'schools/confirm_delete.html', {'object': partnership, 'obj_name': 'Vocational partnership'})
