import re
from django import forms
from datetime import date
from schools.models import School, AcademicSession, Term, Stakeholder, SchoolMetadata, AccreditationStatus, SuspensionClosure, InspectionReport, SchoolMetadata


SCHOOL_TYPE_CHOICES = School.SCHOOL_TYPE_CHOICES
PROGRAM_CHOICES = School.PROGRAM_CHOICES

class SchoolForm(forms.ModelForm):
    """
    Form for creating or updating School instances.
    """
    established_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = School
        exclude = ['id', 'created_at', 'updated_at', 'registration_number']
        widgets = {
            'street_address': forms.TextInput(attrs={'class': 'form-control'}),
            'is_vocational': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'established_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_phone(self):
        phone_number = self.cleaned_data.get('phone')
        pattern = re.compile(r'^(?:\+234|0)?[789]\d{9}$')

        if phone_number and not pattern.match(phone_number):
            raise forms.ValidationError("Enter a valid Nigerian phone number.")
        return phone_number
    

class DateInput(forms.DateInput):
    input_type = 'date'
class AcademicSessionForm(forms.ModelForm):

    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)

    class Meta:
        model = AcademicSession
        fields = ['school_type','program', 'school', 'session_name', 'start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        school_type = cleaned_data.get('school_type')
        school = cleaned_data.get('school')

        if school_type == 'individual' and not school:
            self.add_error('school', 'School must be set if school_type is "individual".')
        elif school_type != 'individual' and school:
            self.add_error('school', 'School must be None if school_type is not "individual".')

        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            self.add_error('end_date', 'End date must be after start date.')

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
  


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['academic_session', 'term_name', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'academic_session': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        
     
class SubjectForm(forms.ModelForm):
   pass


class StakeholderForm(forms.ModelForm):
    class Meta:
        model = Stakeholder
        fields = ['name', 'position', 'phone_number', 'email', 'tenure_start', 'tenure_end', 'profile_picture']
        widgets = {
            'tenure_start': forms.DateInput(attrs={'type': 'date'}),
            'tenure_end': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(StakeholderForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

class SchoolMetadataForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # Dynamically set the initial school value from kwargs
        school_pk = kwargs.pop('school_pk', None)
        super().__init__(*args, **kwargs)
        if school_pk:
            self.fields['school'].initial = school_pk
            
    class Meta:
        model = SchoolMetadata
        fields = [
            'language_of_instruction',
            'enrollment_capacity',
            'ownership_status',
            'owner',
            'compliance_percentage',
        ]
        widgets = {
            'school': forms.HiddenInput(),
            'language_of_instruction': forms.Select(attrs={'class': 'form-control'}),
            'enrollment_capacity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'ownership_status': forms.Select(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. JIBWIS JOS'}),
            'compliance_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '100'}),
        }
        labels = {
            'language_of_instruction': 'Language of Instruction',
            'enrollment_capacity': 'Annual Enrollment Capacity',
            'ownership_status': 'Ownership Status',
            'owner': 'Owner Name',
            'compliance_percentage': 'Compliance Percentage (%)',
        }

    # General percentage validation for all percentage fields (pass_rate, graduation_rate, etc.)
    def clean_percentage_field(self, field_name):
        value = self.cleaned_data.get(field_name)
        if value is not None and (value < 0 or value > 100):
            raise forms.ValidationError(f"{field_name.replace('_', ' ').title()} must be between 0 and 100.")
        return value

    # Applying the percentage validation to the fields
    def clean_compliance_percentage(self):
        return self.clean_percentage_field('compliance_percentage')

    # Custom validation for enrollment capacity to ensure it's a positive number
    def clean_enrollment_capacity(self):
        capacity = self.cleaned_data.get('enrollment_capacity')
        if capacity < 1:
            raise forms.ValidationError("Enrollment capacity must be a positive integer.")
        return capacity


class AccreditationForm(forms.ModelForm):
    class Meta:
        model = AccreditationStatus
        exclude = ['accreditation_number', 'created_at', 'school']
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'valid_to': forms.DateInput(attrs={'type': 'date'}),
          }
    def __init__(self, *args, **kwargs):
        super(AccreditationForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'

class SuspensionForm(forms.ModelForm):
    class Meta:
        model = SuspensionClosure
        exclude = ['created_at', 'updated_at', 'school', 'is_dropped']  
        widgets = {
            'suspended_to': forms.DateInput(attrs={'type': 'date'}),
            'suspended_from': forms.DateInput(attrs={'type': 'date'}),
          }
        labels = {
            'is_statewide': 'Affecting all schools in the state?',
            'is_indefinite': 'Is the suspension indefinite?',
        }
    def __init__(self, *args, **kwargs):
        super(SuspensionForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        self.fields['is_statewide'].widget.attrs.update({'class': 'form-check-input'})
        self.fields['is_indefinite'].widget.attrs.update({'class': 'form-check-input'})
        

class InspectionReportForm(forms.ModelForm):
    class Meta:
        model = InspectionReport
        exclude = ['date_created', 'school']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
          }
        labels = {
            'date': 'Inspection date',
        }
    def __init__(self, *args, **kwargs):
        super(InspectionReportForm, self).__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'



# ===========================
# +++++++++++++++++++++++++++
# |||                     |||
# ||| PARENTAL ENGAGEMENT |||
# |||                     |||
# +++++++++++++++++++++++++++
# ===========================

from schools.models import ParentEngagement

class ParentEngagementForm(forms.ModelForm):
    class Meta:
        model = ParentEngagement
        fields = ["activity_name", "activity_date", "participants_count"]
        widgets = {
            "activity_name": forms.TextInput(attrs={"class": "form-control"}),
            "activity_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "participants_count": forms.NumberInput(attrs={"class": "form-control"}),
        }
