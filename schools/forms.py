from django import forms
from datetime import date
from schools.models import School, AcademicSession, Subject, Term
import re

SCHOOL_TYPE_CHOICES = School.SCHOOL_TYPE_CHOICES
PROGRAM_CHOICES = School.PROGRAM_CHOICES

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'moto', 'school_type', 'lga', 'ward', 'school_email', 'school_phone_number', 'school_website', 'program', 'logo']

    def __init__(self, *args, **kwargs):
        super(SchoolForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['moto'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['school_type'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['lga'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['ward'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['school_email'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['school_phone_number'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['school_website'].widget.attrs.update({'class': 'form-control'})
        self.fields['program'].widget.attrs.update({'class': 'form-control', 'required': 'required'})
        self.fields['logo'].widget.attrs.update({'class': 'form-control'})
    def clean_school_phone_number(self):
        phone_number = self.cleaned_data.get('school_phone_number')
        pattern = re.compile(r'^(?:\+234|0)?[789]\d{9}$')
        if not pattern.match(phone_number): # type: ignore
            raise forms.ValidationError("Enter a valid Nigerian phone number.")
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['name', 'school_type', 'lga', 'ward', 'school_email', 'school_phone_number', 'program']

        for field in required_fields:
            value = cleaned_data.get(field)
            if not value:
                self.add_error(field, "This field is required.")
        
        return cleaned_data

    def clean_school_email(self):
        email = self.cleaned_data.get('school_email')
        if not email:
            raise forms.ValidationError("This field is required.")
        elif not email or '@' not in email or '.' not in email:
            raise forms.ValidationError('Invalid email address')
        return email

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


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = ['academic_session', 'start_date_1', 'end_date_1', 'start_date_2', 'end_date_2', 'start_date_3', 'end_date_3']
        widgets = {
            'start_date_1': forms.DateInput(attrs={'type': 'date', 'label': 'First term start date'}),
            'end_date_1': forms.DateInput(attrs={'type': 'date', 'label': 'First term end date'}),
            'start_date_2': forms.DateInput(attrs={'type': 'date', 'label': 'Second term start date'}),
            'end_date_2': forms.DateInput(attrs={'type': 'date', 'label': 'Second term end date'}),
            'start_date_3': forms.DateInput(attrs={'type': 'date', 'label': 'Third term start date'}),
            'end_date_3': forms.DateInput(attrs={'type': 'date', 'label': 'Third term end date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        instance = kwargs.get('instance')
        if instance:
            self.fields['start_date_1'].initial = instance.start_date_1
            self.fields['end_date_1'].initial = instance.end_date_1
            self.fields['start_date_2'].initial = instance.start_date_2
            self.fields['end_date_2'].initial = instance.end_date_2
            self.fields['start_date_3'].initial = instance.start_date_3
            self.fields['end_date_3'].initial = instance.end_date_3


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name', 'program', 'is_general', 'is_optional', 'school']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['school'].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_general = cleaned_data.get('is_general')
        school = cleaned_data.get('school')

        if not is_general and not school:
            self.add_error('school', 'This field is required for non-general subjects.')

        return cleaned_data
