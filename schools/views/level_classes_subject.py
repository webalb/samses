from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from schools.models import LevelClasses,Stream, School, ProgramLevelTemplate, SubjectRepository, GradingScale, SchoolSubject
from schools.forms import LevelClassesForm, ClassWithoutProgramLevelFieldForm, NoStreamForm, SubjectRepositoryForm, SchoolSubjectForm

def get_class_form(program_level):
    """
    Helper function to determine the appropriate form based on program level.
    """
    if program_level.program != 'sss':
        return NoStreamForm
    return ClassWithoutProgramLevelFieldForm


def level_class_create(request, school_id):
    """
    View to create a new level class for a school.
    """
    school = get_object_or_404(School, pk=school_id)
    form = LevelClassesForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.instance.school = school
        try:
            form.save()
            messages.success(request, "Class created successfully.")
            return redirect('schools:details', pk=school.pk)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            messages.error(request, "Failed to create class. Please correct the errors.")

    return render(request, 'schools/create.html', {
        'object': school,
        'form': form,
        'obj_name': LevelClasses._meta.verbose_name,
    })


def level_class_update(request, pk):
    """
    View to update an existing level class.
    """
    level_class = get_object_or_404(LevelClasses, pk=pk)
    form = LevelClassesForm(request.POST or None, instance=level_class)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, "Class updated successfully.")
            return redirect('schools:details', pk=level_class.school.pk)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            messages.error(request, "Failed to update class. Please correct the errors.")

    return render(request, 'schools/create.html', {
        'object': level_class.school,
        'form': form,
        'obj_name': LevelClasses._meta.verbose_name,
    })


def level_class_delete(request, pk):
    """
    View to delete a level class.
    """
    level_class = get_object_or_404(LevelClasses, pk=pk)
    if request.method == 'POST':
        level_class.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect('schools:details', pk=level_class.school.pk)

    return render(request, 'schools/confirm_delete.html', {
        'school': level_class.school,
        'object': level_class,
        'obj_name': LevelClasses._meta.verbose_name,
    })


def level_classes_create_for_existing(request, level_class_id):
    """
    Create additional classes for an existing program level.
    """
    existing_class = get_object_or_404(LevelClasses, pk=level_class_id)
    form_class = get_class_form(existing_class.program_level_template)
    form = form_class(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_class = form.save(commit=False)
        new_class.school = existing_class.school
        new_class.program_level_template = existing_class.program_level_template
        try:
            new_class.save()
            messages.success(request, "Class added successfully.")
            return redirect('schools:details', pk=existing_class.school.pk)
        except (IntegrityError, ValidationError) as e:
            if isinstance(e, IntegrityError):
                # Extract the specific database error message 
                form.add_error(None, f"Something bad detected from your data, please review and try again") 
            elif isinstance(e, ValidationError):

                for field, errors in e.message_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            messages.error(request, "Failed to add class. Please correct the errors.")

    return render(request, 'schools/create.html', {
        'form': form,
        'object': existing_class.program_level_template,
        'obj_name': 'Level class',
        'school': existing_class.school,
    })


def level_classes_create(request, school_id, program_level_id):
    """
    Create a class for a specific program level.
    """
    school = get_object_or_404(School, pk=school_id)
    program_level = get_object_or_404(ProgramLevelTemplate, pk=program_level_id)
    form_class = get_class_form(program_level)
    form = form_class(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_class = form.save(commit=False)
        new_class.school = school
        new_class.program_level_template = program_level
        try:
            new_class.save()
            messages.success(request, "Class added successfully.")
            return redirect('schools:details', pk=school.pk)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    form.add_error(field, error)
            messages.error(request, "Failed to add class. Please correct the errors.")

    return render(request, 'schools/create.html', {
        'form': form,
        'object': program_level,
        'obj_name': 'Level class',
        'school': school,
    })


# ===========================
# | SUBJECT MANAGEMENT VIEWS|
# ===========================

def subject_list(request):
    subjects = SubjectRepository.objects.all().prefetch_related(
        Prefetch(
            'streams', 
            queryset=Stream.objects.filter(
                id__in=Subquery(
                    Stream.objects.values('name').annotate(
                        max_id=Max('id')
                    ).values('max_id')
                )
            )
        )
    )

    grading_scales = GradingScale.objects.all()

    return render(request, 'schools/subject_list.html', {'subjects': subjects, 'grading_scales': grading_scales})


from django.shortcuts import render, get_object_or_404
from schools.models import SubjectRepository

def subject_detail(request, pk):
    """
    Displays detailed information about a subject, including schools offering it,
    grading configuration, and associated grading scales.
    """
    # Fetch the subject or return a 404 if not found
    subject = get_object_or_404(
        SubjectRepository.objects.prefetch_related(
            'school_subjects__school',  # Fetch related schools offering the subject
            'grading_configurations__grading_scale__grade_boundaries'  # Fetch grading configurations and boundaries
        ),
        pk=pk
    )
    

    # Get schools offering the subject
    # this return the appropriete retult
    schools_offering = School.objects.filter(
        offered_subjects__subject_repository_id=subject.id,
        offered_subjects__is_active=True
    ).distinct()


    # Prepare grading configurations and associated boundaries
    grading_configurations = subject.grading_configurations.first()
    # Context for the template
    context = {
        'subject': subject,
        'schools_offering': schools_offering,
        'grading_configurations': grading_configurations,
    }
    if grading_configurations:
        grading_boundaries = grading_configurations.grading_scale.grade_boundaries.all()
        context = context | {'grading_boundaries': grading_boundaries}

    
    return render(request, 'schools/subject_detail.html', context)

def subject_update(request, pk):
    subject = get_object_or_404(SubjectRepository, pk=pk)
    if request.method == 'POST':
        form = SubjectRepositoryForm(request.POST, instance=subject)
        if form.is_valid():
            subject = form.save(commit=False) 
            subject.save()  # Save the subject to get the ID
            form.save_m2m()
            return redirect('schools:subject_list')  # Redirect after successful edit
    else:
        form = SubjectRepositoryForm(instance=subject)
    return render(request, 'schools/create.html', {'form': form, 'subject': subject})


def subject_create(request):
    if request.method == 'POST':
        form = SubjectRepositoryForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False) 
            subject.save()  # Save the subject to get the ID

                # Perform validation after saving 
   
            form.save_m2m()  # Save many-to-many relationships
            return redirect('schools:subject_list')  # Redirect to the subject list page after creation
    else:
        form = SubjectRepositoryForm()
    return render(request, 'schools/create.html', {'form': form, 'obj_name': 'Subject'})


def subject_delete(request, pk):
    # Get the subject to be deleted
    subject = get_object_or_404(SubjectRepository, pk=pk)

    # Handle form submission for deletion
    if request.method == 'POST':
        # Delete the subject
        subject.delete()
        messages.success(request, 'Subject deleted successfully.')
        return redirect('schools:subject_list')  # Redirect to the subject list page after deletion

    return render(request, 'schools/subject_confirm_delete.html', {'subject': subject})


from django.db.models import Prefetch, Subquery, OuterRef, Max, Q

# List all offered subjects for a school
def school_subject_list(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    
    # Fetch the program levels for this specific school
    school_program_levels = school.program.split('+')

    # Filter subjects for the school, considering only relevant program levels
   

    offered_subjects = school.offered_subjects.select_related(
        'subject_repository'
    ).prefetch_related(
        Prefetch(
            'subject_repository__streams', 
            queryset=Stream.objects.filter(
                id__in=Subquery(
                    Stream.objects.values('name').annotate(
                        max_id=Max('id')
                    ).values('max_id')
                )
            )
        )
    )

    return render(request, 'schools/school_subject_list.html', {
        'school': school,
        'offered_subjects': offered_subjects,
        'school_program_levels': school_program_levels,  # Pass the school program levels to the template
    })

# Add a new subject to the school
def school_subject_create(request, school_id):
    school = get_object_or_404(School, pk=school_id)
    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST)
        if form.is_valid():
            school_subject = form.save(commit=False)
            school_subject.school = school
            school_subject.save()
            form.save_m2m()  # Save Many-to-Many relationships
            messages.success(request, "Subject added successfully.")
            return redirect('schools:school_subject_list', school_id=school.pk)
    else:
        form = SchoolSubjectForm(school=school)

    return render(request, 'schools/create.html', {
        'form': form,
        'object': school,
        'obj_name': 'School Subject',
    })



# Add All Subjects to School Confirmation View
def school_subject_add_all(request, school_id):
    school = get_object_or_404(School, pk=school_id)

    # Split the school's program into components (e.g., 'jss+sss' -> ['jss', 'sss'])
    program_components = school.program.split('+')

    # Fetch related DepartmentRepository objects from SchoolDepartment
    school_departments = school.school_departments.values_list('departments', flat=True)

    # Fetch all subjects for the school
    all_subjects = SubjectRepository.objects.filter(
        Q(category__in=['core', 'religious', 'local_language']) |  # Non-vocational subjects
        Q(
            category='vocational',
            vocational_department__id__in=school_departments  # Use IDs from DepartmentRepository
        )
    ).filter(
        program_levels__program__in=program_components
    ).exclude(
        id__in=school.offered_subjects.values_list('subject_repository', flat=True)
    ).distinct()



    if request.method == 'POST':
        # Add all the remaining subjects to the school
        for subject in all_subjects:
            school.offered_subjects.create(subject_repository=subject)

        return redirect('schools:school_subject_list', school.pk)  # Redirect to the list page after adding subjects

    return render(request, 'schools/school_subject_add_all.html', {
        'school': school,
        'all_subjects': all_subjects,
    })


# Edit an existing school subject
def school_subject_update(request, pk):
    school_subject = get_object_or_404(SchoolSubject, pk=pk)
    school = get_object_or_404(School, pk=school_subject.school.pk)
    if request.method == 'POST':
        form = SchoolSubjectForm(request.POST, instance=school_subject)
        if form.is_valid():
            form.save()
            messages.success(request, "Subject updated successfully.")
            return redirect('schools:school_subject_list', school_id=school_subject.school.pk)
    else:
        form = SchoolSubjectForm(instance=school_subject, school=school)

    return render(request, 'schools/create.html', {
        'form': form,
        'school': school_subject.school,
        'action': 'Edit Subject',
    })

# Delete a school subject
def school_subject_delete(request, pk):
    school_subject = get_object_or_404(SchoolSubject, pk=pk)
    school = school_subject.school
    if request.method == 'POST':
        school_subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect('schools:school_subject_list', school_id=school.pk)

    return render(request, 'schools/confirm_delete.html', {
        'object': school_subject,
        'school': school,
        'obj_name': 'School Subject'
    })
