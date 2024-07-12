from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .forms import SchoolForm, AcademicSessionForm, SubjectForm, TermForm
from .models import School, AcademicSession, Subject, Term

"""
====================================
| VIEWS FOR HANDLING SCHOOL MODEL  |
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin to manupulate the|
|           school model.          |
====================================
"""
@login_required
def school_create(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'School created successfully!')  # Display success message
            return redirect('schools:list')
        else:
            messages.error(request, 'Something bad happens, please review the data you provided')  # Display success message
    else:
        form = SchoolForm()
    return render(request, 'schools/school_create.html', {'form': form})

@login_required
def school_update(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, 'School updated successfully!')  # Display success message
            return redirect('schools:list')
        else:
            messages.error(request, 'Something bad happens, please review the data you provided')  # Display success message
    else:
        form = SchoolForm(instance=school)
    return render(request, 'schools/school_create.html', {'form': form})

@login_required
def school_list(request):
    schools = School.objects.all()
    return render(request, 'schools/school_list.html', {'schools': schools})

@login_required
def school_details(request, pk):
    school = get_object_or_404(School, pk=pk)
    academic_session = school.get_academic_session()
    context = {
        'school': school,
        'academic_session': academic_session,
    }
    return render(request, 'schools/school_details.html', context)

@login_required
def school_delete(request, pk):
    school = get_object_or_404(School, pk=pk)

    # Confirmation check before deletion (optional)
    if request.method == 'POST':
        school.delete()
        messages.success(request, 'School deleted successfully!')  # Display success message
        return redirect('schools:list')  # Redirect to schools list after delete

    return render(request, 'schools/school_confirm_delete.html', {'school': school})

"""
==============================================
| VIEWS FOR HANDLING ACADEMIC SESSION MODEL  |
|                                            |
| Remained: adding user permission to allow  |
|           ministry and schools admin to    |
|           manupulate the school model.     |
==============================================
"""

@login_required
def academic_session_create(request):
    if request.method == 'POST':
        form = AcademicSessionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academic session created successfully')
            return redirect('schools:academic_sessions')
    else:
        form = AcademicSessionForm()
    return render(request, 'schools/academic_session_create.html', {'form': form})

@login_required
def academic_session_update(request, pk):
    academic_session = get_object_or_404(AcademicSession, pk=pk)
    if request.method == 'POST':
        form = AcademicSessionForm(request.POST, instance=academic_session)
        if form.is_valid():
            form.save()
            return redirect('schools:academic_sessions')
    else:
        form = AcademicSessionForm(instance=academic_session)
    return render(request, 'schools/academic_session_create.html', {'form': form})

@login_required
def academic_session_list(request):
    academic_sessions = AcademicSession.objects.all()
    return render(request, 'schools/academic_session_list.html', {'academic_sessions': academic_sessions})

@login_required
def academic_session_delete(request, pk):
    academic_session = get_object_or_404(AcademicSession, pk=pk)

    # Confirmation check before deletion (optional)
    if request.method == 'POST':
        academic_session.delete()
        messages.success(request, 'Academic session deleted successfully!')  # Display success message
        return redirect('schools:academic_sessions')  # Redirect to academic sessions list after delete

    return render(request, 'schools/academic_session_confirm_delete.html', {'session': academic_session})

"""
====================================
|  VIEWS FOR HANDLING TERM MODEL   |
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin to manupulate the|
|           school model.          |
====================================
"""
@login_required
def term_list(request):
    terms = Term.objects.all()
    return render(request, 'schools/term_list.html', {'terms': terms})

@login_required
def term_detail(request, pk):
    term = get_object_or_404(Term, pk=pk)
    return render(request, 'schools/term_detail.html', {'term': term})

@login_required
def term_create(request):
    if request.method == "POST":
        form = TermForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('schools:term_list')
    else:
        form = TermForm()
    return render(request, 'schools/term_create.html', {'form': form})

@login_required
def term_update(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == "POST":
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            return redirect('schools:term_list')
    else:
        form = TermForm(instance=term)
    return render(request, 'schools/term_create.html', {'form': form})

@login_required
def term_delete(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == "POST":
        term.delete()
        return redirect('schools:term_list')
    return render(request, 'schools/term_confirm_delete.html', {'term': term})

"""
====================================
|  VIEWS FOR HANDLING SUBJECT MODEL|
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin to manupulate the|
|           subject model.          |
====================================
"""
@login_required
def subject_list(request):
    if request.user.is_ministry_admin:
        subjects = Subject.objects.all()
    else:
        subjects = Subject.objects.filter(school=request.user.school) | Subject.objects.filter(is_general=True)
    return render(request, 'schools/subject_list.html', {'subjects': subjects})

@login_required
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'schools/subject_detail.html', {'subject': subject})

@login_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('schools:subject_list')
    else:
        form = SubjectForm(user=request.user)
    return render(request, 'schools/subject_create.html', {'form': form})

@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('schools:subject_list')
    else:
        form = SubjectForm(instance=subject, user=request.user)
    return render(request, 'schools/subject_create.html', {'form': form})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect('schools:subject_list')
    return render(request, 'schools/subject_confirm_delete.html', {'subject': subject})
