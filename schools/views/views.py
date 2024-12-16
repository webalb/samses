from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from itertools import zip_longest
from django.views.generic.edit import FormView

from schools.forms import SchoolForm, AcademicSessionForm, SubjectForm, TermForm, StakeholderForm
from schools.models import School, AcademicSession, Subject, Term, Stakeholder, Classrooms, SchoolImages

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
            new_school = form.save(commit=False)  # Don't save to the database yet
            new_school.pk = None  # Explicitly set the pk to None, so it's a new object
            new_school.save()  # Now save it, and Django will generate the pk
            messages.success(request, 'School created successfully!')  # Display success message
            return redirect('schools:details', pk=new_school.pk)
        else:
            messages.error(request, 'Something bad happens, please review the data you provided')  # Display success message
    else:
        form = SchoolForm()
        form.instance.pk = None
    return render(request, 'schools/school_create.html', {'form': form})

@login_required
def school_update(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        form = SchoolForm(request.POST, request.FILES, instance=school)
        if form.is_valid():
            form.save()
            messages.success(request, 'School updated successfully!')  # Display success message
            return redirect('schools:details', pk=pk)
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
    stakeholders = school.stakeholders.all()
    classroom = Classrooms.objects.filter(school=school).order_by('-created_at').first()  # Expecting only one record

    # Fetch images grouped by type
    classroom_images = SchoolImages.objects.filter(school=school, image_type='classroom').order_by('-created_at')[:3]
   
    context = {
        'school': school,
        'academic_session': academic_session,
        'stakeholders': stakeholders,
        'classroom': classroom,
        'classroom_images': classroom_images,
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
def term_create_or_update(request, academic_session_id):
    academic_session = get_object_or_404(AcademicSession, id=academic_session_id)
    term, created = Term.objects.get_or_create(academic_session=academic_session)

    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, 'Term details saved successfully!')
            return redirect('schools:academic_sessions')  # Redirect to the appropriate view after saving
    else:
        form = TermForm(instance=term)
    
    return render(request, 'schools/term_create.html', {'form': form, 'academic_session': academic_session})


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
def subject_detail(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, 'schools/subject_detail.html', {'subject': subject})

@login_required
def subject_create(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject added successfully!')
            return redirect('schools:subject_list')
    else:
        form = SubjectForm()
    return render(request, 'schools/subject_create.html', {'form': form})

@login_required
def subject_list(request):
    subjects = Subject.objects.all()
    primary_subjects = list(subjects.filter(program='primary'))
    jss_subjects = list(subjects.filter(program='jss'))
    sss_subjects = list(subjects.filter(program='sss'))

    # Use zip_longest to handle programs with different numbers of subjects
    subject_rows = list(zip_longest(primary_subjects, jss_subjects, sss_subjects, fillvalue=None)) # type: ignore

    return render(request, 'schools/subject_list.html', {'subject_rows': subject_rows})

@login_required
def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        form = SubjectForm(request.POST, instance=subject,)
        if form.is_valid():
            form.save()
            return redirect('schools:subject_list')
    else:
        form = SubjectForm(instance=subject,)
    return render(request, 'schools/subject_create.html', {'form': form})

@login_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == "POST":
        subject.delete()
        return redirect('schools:subject_list')
    return render(request, 'schools/subject_confirm_delete.html', {'subject': subject})


"""
====================================
|  VIEWS FOR HANDLING Stakeholder MODEL|
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin and school admins to manupulate the|
|           stakeholder model.          |
====================================
"""

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView


@login_required
def stakeholder_create(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        form = StakeholderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stakeholder added successfully!')
            form = StakeholderForm()
            stakeholders = Stakeholder.objects.filter(school=school.id)
            return render(request, 'schools/stakeholder_form.html', {'form': form, 'stakeholders': stakeholders, 'school': school})
    else:
        form = StakeholderForm()
    stakeholders = Stakeholder.objects.filter(school=school.id)
    return render(request, 'schools/stakeholder_form.html', {'form': form, 'stakeholders': stakeholders, 'school': school})


@login_required
def stakeholder_update(request, pk):
    stakeholder = get_object_or_404(Stakeholder, pk=pk)
    if request.method == "POST":
        form = StakeholderForm(request.POST, instance=stakeholder)
        if form.is_valid():
            form.save()
            print("Stakeholder %s updated successfully!" % stakeholder.stakeholder_name)
            messages.success(request, 'Stakeholder updated successfully!')
            form = StakeholderForm()
            stakeholders = Stakeholder.objects.filter(school=stakeholder.school.id)
            return render(request, 'schools/stakeholder_form.html', {'form': form, 'stakeholders': stakeholders, 'school': stakeholder.school})
    form = StakeholderForm(instance=stakeholder)
    stakeholders = Stakeholder.objects.filter(school=stakeholder.school.id)
    context =  {'form': form, 'stakeholders': stakeholders, 'school': stakeholder.school, 'stakeholder': stakeholder}
    return render(request, 'schools/stakeholder_form.html', context)

@login_required
def stakeholder_delete(request, pk):
    stakeholder = get_object_or_404(Stakeholder, pk=pk)
    if request.method == "POST":
        stakeholder.delete()
        return redirect('schools:stakeholder_create', pk=stakeholder.school.id)
    return render(request, 'schools/stakeholder_confirm_delete.html', {'stakeholder': stakeholder})

"""
====================================
|VIEWS FOR SchoolMetadata MODEL    |
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin to manupulate the|
|           Metadata model.        |
====================================
"""
from schools.forms import SchoolMetadataForm
from schools.models import SchoolMetadata
@login_required
def metadata_set(request, pk):
    school = get_object_or_404(School, pk=pk,)
    if request.POST:
        form = SchoolMetadataForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Metadata set successfully!")
            return redirect('schools:details', pk=pk)
    else:
        form = SchoolMetadataForm(initial={'school': school})
    return render(request, 'schools/metadata_form.html', {'form': form, 'school': school})

@login_required
def metadata_update(request, pk):
    metadata = get_object_or_404(SchoolMetadata, pk=pk)
    if request.POST:
        form = SchoolMetadataForm(request.POST, instance=metadata)
        if form.is_valid():
            form.save()
            messages.success(request, "Metadata updated successfully.")
            return redirect("schools:details", pk=metadata.school.pk)
    form = SchoolMetadataForm(instance=metadata)
    return render(request, "schools/metadata_form.html", {'form': form, 'school': metadata.school })

@login_required
def metadata_delete(request, pk):
    metadata = get_object_or_404(SchoolMetadata, pk=pk)
    if request.POST:
        metadata.delete()
        return redirect("schools:details", pk=metadata.school.pk)
    return render(request, 'schools/metadata_confirm_delete.html', {'metadata': metadata})

"""
====================================
|VIEWS FOR Accreditation status MODEL|
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin to manupulate the|
|           Metadata model.        |
====================================
"""
from schools.models import AccreditationStatus
from schools.forms import AccreditationForm

@login_required
def accreditation_set(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.POST:
        form = AccreditationForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, "Accreditation set successfully for this school.")
            return redirect("schools:details", pk=pk)
        else:
            return render(request, "schools/accreditation_form.html", {'form': form, 'school': school})


    form = AccreditationForm()
    return render(request, "schools/accreditation_form.html", {'form': form, 'school': school})

@login_required
def accreditation_update(request, pk):
    accr = get_object_or_404(AccreditationStatus, pk=pk)
    if request.POST:
        form = AccreditationForm(request.POST, instance=accr, initial={'school': school.pk})
        if form.is_valid():
            form.save()
            messages.success(request, "Accreditation updated successfully for this school")
            return redirect("schools:details", pk=accr.school.pk)
    form = AccreditationForm(instance=accr)
    return render(request, "schools/accreditation_form.html", {'form': form,'school': accr.school})
@login_required
def accreditation_delete(request, pk):
    accr = get_object_or_404(AccreditationStatus, pk=pk)
    if request.POST:
        accr.delete()
        return redirect("schools:details", pk=accr.school.pk)
    return render(request, 'schools/accreditation_confirm_delete.html', {'accreditation': accr})

"""
====================================
|VIEWS FOR Suspension closure MODEL|
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin to manupulate the|
|            model.        |
====================================
"""
from schools.models import SuspensionClosure
from schools.forms import SuspensionForm
@login_required
def suspension_set(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.POST:
        form = SuspensionForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, "School suspended successfully.")
            return redirect("schools:details", pk=pk)
        else:
            return render(request, "schools/suspension_form.html", {'form': form, 'school': school})


    form = SuspensionForm()
    return render(request, "schools/suspension_form.html", {'form': form, 'school': school})

@login_required
def suspension_update(request, pk):
    suspension = get_object_or_404(SuspensionClosure, pk=pk)
    if request.POST:
        form = SuspensionForm(request.POST, instance=suspension, initial={'school': school.pk})
        if form.is_valid():
            form.save()
            messages.success(request, "Suspension updated successfully for this school")
            return redirect("schools:details", pk=suspension.school.pk)
    form = SuspensionForm(instance=accr)
    return render(request, "schools/suspension_form.html", {'form': form,'school': suspension.school})
@login_required
def suspension_drop(request, pk):
    suspension = get_object_or_404(SuspensionClosure, pk=pk)
    if request.POST:
        suspension.is_dropped = True
        suspension.save()
        messages.success(request, "Suspension dropped successfully for this school")
        return redirect("schools:details", pk=suspension.school.pk)
    return render(request, 'schools/suspension_confirm_delete.html', {'suspension': suspension})

"""
====================================
|VIEWS FOR inspection report MODEL |
|                                  |
| Remained: adding user permission |
|           to allow only ministry |
|           admin to manupulate the|
|            model.        |
====================================
"""
from schools.models import InspectionReport
from schools.forms import InspectionReportForm
@login_required
def inspection_report_set(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.POST:
        form = InspectionReportForm(request.POST,)
        if form.is_valid():
            form.save()
            messages.success(request, "Inspection report added successfully.")
            return redirect("schools:details", pk=pk)
        else:
            return render(request, "schools/inspection_report_form.html", {'form': form, 'school': school})


    form = InspectionReportForm()
    return render(request, "schools/inspection_report_form.html", {'form': form, 'school': school})

@login_required
def inspection_report_update(request, pk):
    inspection_report = get_object_or_404(InspectionReport, pk=pk)
    if request.POST:
        form = InspectionReportForm(request.POST, instance=inspection_report,)
        if form.is_valid():
            form.save()
            messages.success(request, "Inspection report updated successfully for this school")
            return redirect("schools:details", pk=inspection_report.school.pk)
    form = InspectionReportForm(instance=inspection_report)
    return render(request, "schools/inspection_report_form.html", {'form': form,'school': inspection_report.school})
@login_required
def inspection_report_delete(request, pk):
    inspection_report = get_object_or_404(InspectionReport, pk=pk)
    if request.POST:
        inspection_report.delete()
        return redirect("schools:details", pk=inspection_report.school.pk)
    return render(request, 'schools/inspection_report_confirm_delete.html', {'inspection_report': inspection_report})
