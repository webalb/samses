from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from backend.schools.models import GradingScale, GradeBoundary, SubjectGradingConfiguration, SubjectRepository
from backend.schools.forms import GradingScaleForm, GradeBoundaryForm, SubjectGradingConfigurationForm


def grading_scale_create(request):
    if request.method == 'POST':
        form = GradingScaleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grading Scale created successfully.')
            return redirect('schools:subject_list')
    else:
        form = GradingScaleForm()
    return render(request, 'schools/create.html', {'form': form, 'obj_name': 'Grading Scale'})

def grading_scale_update(request, pk):
    grading_scale = get_object_or_404(GradingScale, pk=pk)
    if request.method == 'POST':
        form = GradingScaleForm(request.POST, instance=grading_scale)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grading Scale updated successfully.')
            return redirect('schools:subject_list')
    else:
        form = GradingScaleForm(instance=grading_scale)
    return render(request, 'schools/create.html', {'form': form, 'object': grading_scale, 'obj_name': 'Grading Scale'})

def grading_scale_delete(request, pk):
    grading_scale = get_object_or_404(GradingScale, pk=pk)
    if request.method == 'POST':
        grading_scale.delete()
        messages.success(request, 'Grading Scale deleted successfully.')
        return redirect('schools:subject_list')
    return render(request, 'schools/confirm_delete.html', {'object': grading_scale, 'obj_name': 'Grading Scale'})

def grading_scale_detail(request, pk):
    grading_scale = get_object_or_404(GradingScale, pk=pk)
    grade_boundaries = grading_scale.grade_boundaries.all()

    return render(request, 'schools/grading_scale_boundaries.html', {
        'grading_scale': grading_scale,
        'grade_boundaries': grade_boundaries,
        })

# =============================
# ||| GRADING SCALE BOUNDARY|||
# =============================

def grade_boundary_create(request, grading_scale_id):
    grading_scale = get_object_or_404(GradingScale, pk=grading_scale_id)
    if request.method == 'POST':
        form = GradeBoundaryForm(request.POST)
        if form.is_valid():
            grade_boundary = form.save(commit=False)
            grade_boundary.grading_scale = grading_scale
            grade_boundary.save()
            messages.success(request, 'Grade Boundary created successfully.')
            return redirect('schools:grading_scale_detail', pk=grading_scale.id)
    else:
        form = GradeBoundaryForm()
    return render(request, 'schools/create.html', {
        'form': form,
        'object': grading_scale,
        'obj_name': 'Grade Boundary',
    })

def grade_boundary_update(request, pk):
    grade_boundary = get_object_or_404(GradeBoundary, pk=pk)
    grading_scale = grade_boundary.grading_scale
    if request.method == 'POST':
        form = GradeBoundaryForm(request.POST, instance=grade_boundary)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade Boundary updated successfully.')
            return redirect('schools:grading_scale_detail', pk=grading_scale.id)
    else:
        form = GradeBoundaryForm(instance=grade_boundary)
    return render(request, 'schools/create.html', {
        'form': form,
        'object': grading_scale,
        'obj_name': 'Grade Boundary',
    })

def grade_boundary_delete(request, pk):
    grade_boundary = get_object_or_404(GradeBoundary, pk=pk)
    if request.method == 'POST':
        grade_boundary.delete()
        messages.success(request, 'Grade Boundary deleted successfully.')
        return redirect('schools:grading_scale_detail', pk=grade_boundary.grading_scale.id)
    return render(request, 'schools/confirm_delete.html', {
        'object': grade_boundary,
        'obj_name': 'Grade Boundary',
    })

# ===================================
# ||| SUBJECT GRADING SCALE SYSTEM|||
# ===================================

def subject_grading_list(request, subject_id):
    subject = get_object_or_404(SubjectRepository, pk=subject_id)
    grading_configurations = subject.grading_configurations.all()
    return render(request, 'schools/subject_grading_list.html', {
        'subject': subject,
        'grading_configurations': grading_configurations
    })

def subject_grading_create(request, subject_id):
    subject = get_object_or_404(SubjectRepository, pk=subject_id)
    if request.method == 'POST':
        form = SubjectGradingConfigurationForm(request.POST)
        if form.is_valid():
            grading_config = form.save(commit=False)
            grading_config.subject = subject
            grading_config.save()
            messages.success(request, 'Grading configuration created successfully.')
            return redirect('schools:subject_detail', pk=subject.id)
    else:
        form = SubjectGradingConfigurationForm()
    return render(request, 'schools/create.html', {
        'form': form,
        'object': subject,
        'obj_name': 'Configure Subject Grading',
    })

def subject_grading_update(request, pk):
    grading_config = get_object_or_404(SubjectGradingConfiguration, pk=pk)
    subject = grading_config.subject
    if request.method == 'POST':
        form = SubjectGradingConfigurationForm(request.POST, instance=grading_config)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grading configuration updated successfully.')
            return redirect('schools:subject_detail', pk=subject.id)
    else:
        form = SubjectGradingConfigurationForm(instance=grading_config)
    return render(request, 'schools/create.html', {
        'form': form,
        'object': subject,
        'obj_name': 'Configure Subject Grading',
    })

def subject_grading_delete(request, pk):
    grading_config = get_object_or_404(SubjectGradingConfiguration, pk=pk)
    if request.method == 'POST':
        grading_config.delete()
        messages.success(request, 'Grading configuration deleted successfully.')
        return redirect('schools:subject_detail', pk=grading_config.subject.id)
    return render(request, 'schools/confirm_delete.html', {
        'object': grading_config,
        'obj_name': 'Subject Grading Configuration',
    })


def configure_grading_scales_all(request):
    """
    View to allow the user to select a grading scale and apply it to all unconfigured subjects.
    """
    if request.method == 'POST':
        # Get the selected grading scale
        scale_id = request.POST.get('grading_scale')
        if not scale_id:
            messages.error(request, "Please select a grading scale.")
            return redirect('schools:configure_grading_scales_all')

        grading_scale = GradingScale.objects.filter(id=scale_id).first()
        if not grading_scale:
            messages.error(request, "Invalid grading scale selected.")
            return redirect('schools:configure_grading_scales_all')

        # Fetch all subjects without grading configurations
        unconfigured_subjects = SubjectRepository.objects.exclude(
            grading_configurations__grading_scale=grading_scale
        )

        # Create configurations for each unconfigured subject
        for subject in unconfigured_subjects:
            SubjectGradingConfiguration.objects.get_or_create(
                subject=subject,
                grading_scale=grading_scale,
                defaults={"weightage": 100.00},  # Default weightage
            )

        messages.success(
            request,
            f"Grading scale '{grading_scale.scale_name}' applied to {unconfigured_subjects.count()} subject(s).",
        )
        return redirect('schools:subject_list')

    # GET: Render the form with available grading scales
    grading_scales = GradingScale.objects.all()
    return render(request, 'schools/configure_grading_scale.html', {'grading_scales': grading_scales})

