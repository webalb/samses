from itertools import zip_longest
from django.contrib import messages
from django.db.models import Q, Prefetch
from django.views.generic.edit import FormView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render

from schools.forms import (
    AcademicSessionForm,
    SchoolForm,
    StakeholderForm,
    SubjectForm,
    TermForm,
)
from schools.models import (
    AcademicSession,
    Classrooms,
    ComputerLab,
    Laboratory,
    Library,
    ProgramLevelTemplate,
    School,
    SchoolImages,
    SportsFacility,
    Stakeholder,
    Stream,
    SpecialNeedsResource,
    Term,
)


# ========================================
# ||| VIEWS FOR HANDLING SCHOOL MODEL  |||
# ========================================

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

    # Infrastructure
    classroom = Classrooms.objects.filter(school=school).order_by('-created_at').first()  # Expecting only one record
    computer_lab = ComputerLab.objects.filter(school=school).order_by('-created_at').first()  # Expecting only one record
    library = Library.objects.filter(school=school).order_by('-created_at').first()
    laboratory = Laboratory.objects.filter(school=school).order_by('-created_at').first()
    sports_facility = SportsFacility.objects.filter(school=school).order_by('-created_at').first()
    special_needs = SpecialNeedsResource.objects.filter(school=school).order_by('-created_at').first()
    # Fetch images grouped by type
    classroom_images = SchoolImages.objects.filter(school=school, image_type='classrooms').order_by('-created_at')[:3]
    computer_lab_images = SchoolImages.objects.filter(school=school, image_type='computerlab').order_by('-created_at')[:3]
    library_images = SchoolImages.objects.filter(school=school, image_type='library').order_by('-created_at')[:3]
    laboratory_images = SchoolImages.objects.filter(school=school, image_type='laboratoty').order_by('-created_at')[:3]
    sports_facility_images = SchoolImages.objects.filter(school=school, image_type='sports_facility').order_by('-created_at')[:3]
    special_needs_images = SchoolImages.objects.filter(school=school, image_type='special_needs_resource').order_by('-created_at')[:3]

    # Fetch the related ProgramLevelTemplate objects
    level_classes = school.get_levels_and_classes()
    
    context = {
        'school': school,
        'academic_session': academic_session,
        'stakeholders': stakeholders,

        'classroom': classroom,
        'classroom_images': classroom_images,
        'computer_lab': computer_lab,
        'computer_lab_images': computer_lab_images,
        'library': library,
        'library_images': library_images,
        'laboratory': laboratory,
        'laboratory_images': laboratory_images,
        'sports_facility': sports_facility,
        'sports_facility_images': sports_facility_images,
        'special_needs': special_needs,
        'special_needs_images': special_needs_images,
    } 
    context = context | level_classes
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
def term_detail(request, pk):
    term = get_object_or_404(Term, pk=pk)
    return render(request, 'schools/term_detail.html', {'term': term})

@login_required
def term_create(request, academic_session_id):
    academic_session = get_object_or_404(AcademicSession, id=academic_session_id)
    
    if request.method == 'POST':
        form = TermForm(request.POST)

        if form.is_valid():
            term = form.save(commit=False)
            term.academic_session = academic_session
            term.save()
            messages.success(request, 'Term created successfully!')
            return redirect('schools:academic_sessions')  # Redirect after creation
    else:
        form = TermForm(initial={'academic_session': academic_session})  # Create an empty form
    
    return render(request, 'schools/term_form.html', {'form': form, 'academic_session': academic_session})

@login_required
def term_update(request, pk):
    # Fetch the term to update or return a 404 if not found
    term = get_object_or_404(Term, pk=pk)
    
    if request.method == 'POST':
        form = TermForm(request.POST, instance=term)
        if form.is_valid():
            # Save changes to the term
            form.save()
            messages.success(request, 'Term updated successfully!')
            return redirect('schools:academic_sessions')  # Redirect after update
    else:
        # Populate the form with the term instance
        form = TermForm(instance=term)
        form.fields['academic_session'].widget.attrs['value'] = term.academic_session.pk  # Set field value directly

    # Render the update form
    return render(request, 'schools/term_form.html', {'form': form, 'academic_session': term.academic_session})

@login_required
def term_delete(request, pk):
    term = get_object_or_404(Term, pk=pk)
    if request.method == "POST":
        term.delete()
        return redirect('schools:academic_sessions')
    return render(request, 'schools/term_confirm_delete.html', {'term': term})

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

@login_required
def stakeholder_create(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == 'POST':
        form = StakeholderForm(request.POST)
        if form.is_valid():
            stakeholder = form.save(commit=False)
            stakeholder.school = school
            stakeholder.save()
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
            meta = form.save(commit=False)
            meta.school_id=school.id
            meta.save()
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
            instance = form.save(commit=False)
            instance.school_id=pk
            instance.save()
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
        form = AccreditationForm(request.POST, instance=accr, initial={'school': accr.school})
        if form.is_valid():
            instance = form.save(commit=False)
            instance.school_id=accr.school_id
            instance.save()
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
            instance = form.save(commit=False)
            instance.school_id=school.pk
            instance.save()            
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
    form = SuspensionForm(instance=suspension)
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
            instance = form.save(commit=False)
            instance.school_id=pk
            instance.save()            
            messages.success(request, "Inspection report added successfully.")
            return redirect("schools:details", pk=pk)
        else:
            return render(request, "schools/inspection_report_form.html", {'form': form, 'school': school})


    form = InspectionReportForm()
    return render(request, "schools/inspection_report_form.html", {'form': form, 'school': school})

@login_required
def inspection_report_all(request, school_id):
    reports = get_list_or_404(InspectionReport, school_id=school_id)
    return render(request, 'schools/reports.html', {'reports': reports})

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


# ===========================
# +++++++++++++++++++++++++++
# |||                     |||
# ||| PARENTAL ENGAGEMENT |||
# |||                     |||
# +++++++++++++++++++++++++++
# ===========================

from schools.models import ParentEngagement
from schools.forms import ParentEngagementForm

def parent_engagement_create(request, pk):
    school = get_object_or_404(School, pk=pk)
    if request.method == "POST":
        form = ParentEngagementForm(request.POST)
        if form.is_valid():
            engagement = form.save(commit=False)
            engagement.school = school
            engagement.save()
            messages.success(request, "Parent engagement activity added successfully.")
            return redirect("schools:details", pk=pk)
    else:
        form = ParentEngagementForm()
    return render(request, "schools/create.html", {"form": form, "object": school, 'obj_name': 'Parent Engagement'})

def parent_engagement_update(request, pk):
    engagement = get_object_or_404(ParentEngagement, pk=pk)
    if request.method == "POST":
        form = ParentEngagementForm(request.POST, instance=engagement)
        if form.is_valid():
            form.save()
            messages.success(request, "Parent engagement activity updated successfully.")
            return redirect("schools:details", pk=engagement.school.pk)
    else:
        form = ParentEngagementForm(instance=engagement)
    return render(request, "schools/create.html", {"form": form, "object": engagement, 'obj_name': 'Parent Engagement'})

def parent_engagement_delete(request, pk):
    engagement = get_object_or_404(ParentEngagement, pk=pk)
    school_id = engagement.school.pk
    if request.method == "POST":
        engagement.delete()
        messages.success(request, "Parent engagement activity deleted successfully.")
        return redirect("schools:details", pk=school_id)
    return render(request, "schools/confirm_delete.html", {"object": engagement, "obj_name": "Parent Engagement"})
