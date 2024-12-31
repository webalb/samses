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
        fields = ['number_of_classrooms', 'classrooms_availability',]

class ClassroomsUpdateForm(ClassroomsForm):
    class Meta(ClassroomsForm.Meta):
        include = ClassroomsForm.Meta.fields + ['images_description']



class LibraryForm(forms.ModelForm):
    """
    Form for adding/editing library details with images.
    """
    class Meta:
        model = Library
        fields = ['book_count', 'digital_access', 'study_space_capacity', 'library_availability',]

class LibraryUpdateForm(LibraryForm):
    class Meta(LibraryForm.Meta):
        fields = LibraryForm.Meta.fields + ['images_description']



class LaboratoryForm(forms.ModelForm):
    """
    Form for adding/editing laboratory details with images.
    """
    class Meta:
        model = Laboratory
        fields = ['lab_type', 'lab_equipment', 'lab_availability',]

class LaboratoryUpdateForm(LaboratoryForm):
    class Meta(LaboratoryForm.Meta):
        fields = LaboratoryForm.Meta.fields + ['images_description']



class ComputerLabForm(forms.ModelForm):
    """
    Form for adding/editing computer lab details with images.
    """
    class Meta:
        model = ComputerLab
        fields = ['number_of_computers', 'internet_access', 'smart_classrooms', 'computer_lab_availability',]
class ComputerLabUpdateForm(ComputerLabForm):
    class Meta(ComputerLabForm.Meta):
        fields = ComputerLabForm.Meta.fields + ['images_description']



class SportsFacilityForm(forms.ModelForm):
    """
    Form for adding/editing sports facility details with images.
    """
    class Meta:
        model = SportsFacility
        fields = ['facility_type', 'field_availability',]

class SportsFacilityUpdateForm(SportsFacilityForm):
    class Meta(SportsFacilityForm.Meta):
        fields =SportsFacilityForm.Meta.fields + ['images_description']


# Image Form to handle image upload and description
class SchoolImagesForm(forms.ModelForm):
    """
    Form for uploading images with description, shared by all infrastructure types.
    """
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False, help_text="Optional description for the images.")
    image = MultipleFileField()
    class Meta:
        model = SchoolImages
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)       
        self.fields['image'].required = False 

# Image Form to handle image  upload without the description field
class SchoolImagesUpdateForm(SchoolImagesForm):
    """
    Form for uploading images without description (description is already available), shared by all infrastructure types.
    """
    description = None



# ==============================
# ||| Special needs resouces |||
# ==============================

from schools.models import SpecialNeedsResource

class SpecialNeedsResourceForm(forms.ModelForm):
    class Meta:
        model = SpecialNeedsResource
        fields = ['resource_name', 'category', 'quantity', 'description', 'urgency_level']
        widgets = {
            'resource_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'urgency_level': forms.Select(attrs={'class': 'form-control'}),
        }

class SpecialNeedsResourceUpdateForm(SpecialNeedsResourceForm):
    class Meta(SpecialNeedsResourceForm.Meta):
        fields =SpecialNeedsResourceForm.Meta.fields + ['images_description']

