from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib import messages
from django.core.exceptions import ValidationError


from backend.schools.models import School, Classrooms, Library, Laboratory, ComputerLab, SportsFacility, SchoolImages
from backend.schools.forms import ( ClassroomsForm, SchoolImagesUpdateForm, LibraryForm, LaboratoryForm, ComputerLabForm, 
        SportsFacilityForm, SchoolImagesForm, LibraryUpdateForm, LaboratoryUpdateForm,
         ComputerLabUpdateForm, SportsFacilityUpdateForm )
from backend.schools.utils import infrastructure_create, infrastructure_update, infrastructure_delete

# Classrooms Create View
def classroom_create(request, school_id):
    """
    View to handle the creation of classroom infrastructure and associated images.
    """
    from backend.schools.forms import ClassroomsForm  # Import form locally if needed
    return infrastructure_create(request, school_id, ClassroomsForm, 'classrooms')

def classroom_update(request, school_id):
    """
    View to handle the update of classroom infrastructure and associated images.
    """
    return infrastructure_update(
        request,
        school_id=school_id,
        model_class=Classrooms,  # Pass the model class
        form_class=ClassroomsUpdateForm,  # Pass the form class
        image_type='classroom'  # Specify the image type
    )

def classroom_delete(request, school_id):
    """
    View to handle the deletion of classroom infrastructure and associated images.
    """
    return infrastructure_delete(
        request=request,
        school_id=school_id,
        model_class=Classrooms,  # Pass the model class
        image_type='classroom',  # Specify the image type
    )
# Specific view for computer lab creation
def computer_lab_create(request, school_id):
    return infrastructure_create(request, school_id, ComputerLabForm, 'computer_lab')

def computer_lab_update(request, school_id):
    """
    View to handle the update of computer lab infrastructure and associated images.
    """
    return infrastructure_update(
        request,
        school_id=school_id,
        model_class=ComputerLab,
        form_class=ComputerLabForm,
        image_type='computer_lab'
    )

def computer_lab_delete(request, school_id):
    """
    View to handle the deletion of computer lab infrastructure and associated images.
    """
    return infrastructure_delete(
        request=request,
        school_id=school_id,
        model_class=ComputerUpdateLabs,  # Pass the model class
        image_type='computer_lab',  # Specify the image type
    )


def laboratory_create(request, school_id):
    return infrastructure_create(request, school_id, LaboratoryForm, 'laboratory')
def laboratory_update(request, school_id):
    return infrastructure_update(
        request,
        school_id=school_id,
        model_class=Laboratory,
        form_class=LaboratoryUpdateForm,
        image_type='laboratory'
    )

def laboratory_delete(request, school_id):
    return infrastructure_delete(
        request=request,
        school_id=school_id,
        model_class=Laboratory,  # Pass the model class
        image_type='laboratory',  # Specify the image type
    )

# Sport Facility Create View
def sports_facility_create(request, school_id):
    return infrastructure_create(
        request=request,
        school_id=school_id,
        form_class=SportsFacilityForm,
        image_type='sports_facility'
    )

# Sport Facility Update View
def sports_facility_update(request, school_id):
    return infrastructure_update(
        request=request,
        school_id=school_id,
        model_class=SportsFacility,
        form_class=SportsFacilityUpdateForm,
        image_type='sports_facility',
    )

# Sport Facility Delete View
def sports_facility_delete(request, school_id):
    return infrastructure_delete(
        request=request,
        school_id=school_id,
        model_class=SportsFacility,
        image_type='sports_facility',
    )

# Library Create View
def library_create(request, school_id):
    return infrastructure_create(
        request=request,
        school_id=school_id,
        form_class=LibraryForm,
        image_type='library'
    )

# Library Update View
def library_update(request, school_id):
    return infrastructure_update(
        request=request,
        school_id=school_id,
        model_class=Library,
        form_class=LibraryUpdateForm,
        image_type='library',
    )

# Library Delete View
def library_delete(request, school_id):
    return infrastructure_delete(
        request=request,
        school_id=school_id,
        model_class=Library,
        image_type='library',
    )
from backend.schools.forms import SpecialNeedsResourceForm, SpecialNeedsResourceUpdateForm
from backend.schools.models import SpecialNeedsResource
# ==============================
# ||| Special needs resouces |||
# ==============================

# Library Create View
def special_needs_create(request, school_id):
    return infrastructure_create(
        request=request,
        school_id=school_id,
        form_class=SpecialNeedsResourceForm,
        image_type='special_needs_resource'
    )

# Library Update View
def special_needs_update(request, school_id):
    return infrastructure_update(
        request=request,
        school_id=school_id,
        model_class=SpecialNeedsResource,
        form_class=SpecialNeedsResourceUpdateForm,
        image_type='special_needs_resource',
    )

# Library Delete View
def special_needs_delete(request, school_id):
    return infrastructure_delete(
        request=request,
        school_id=school_id,
        model_class=SpecialNeedsResource,
        image_type='special_needs_resource',
    )