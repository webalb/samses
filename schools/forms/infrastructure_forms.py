from django import forms
from django.forms import modelformset_factory


from schools.models import Classrooms, Library, Laboratory, ComputerLab, SportsFacility, SchoolImages


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

# Infrastructure Forms

class ClassroomsForm(forms.ModelForm):
    """
    Form for adding/editing classroom details with images.
    """
    class Meta:
        model = Classrooms
        fields = ['number_of_classrooms', 'classrooms_availability', 'images_description']
        widgets = {'images_description': forms.TextInput()}

class LibraryForm(forms.ModelForm):
    """
    Form for adding/editing library details with images.
    """
    class Meta:
        model = Library
        fields = ['book_count', 'digital_access', 'study_space_capacity', 'library_availability']

class LaboratoryForm(forms.ModelForm):
    """
    Form for adding/editing laboratory details with images.
    """
    class Meta:
        model = Laboratory
        fields = ['lab_type', 'lab_equipment', 'lab_availability']

class ComputerLabForm(forms.ModelForm):
    """
    Form for adding/editing computer lab details with images.
    """
    class Meta:
        model = ComputerLab
        fields = ['number_of_computers', 'internet_access', 'smart_classrooms', 'computer_lab_availability']

class SportsFacilityForm(forms.ModelForm):
    """
    Form for adding/editing sports facility details with images.
    """
    class Meta:
        model = SportsFacility
        fields = ['facility_type', 'field_availability']

# Image Form to handle image upload and description
class SchoolImagesForm(forms.ModelForm):
    """
    Form for uploading images with description, shared by all infrastructure types.
    """
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False, help_text="Optional description for the images.")
    image = MultipleFileField()
    class Meta:
        model = SchoolImages
        fields = ['image']

    