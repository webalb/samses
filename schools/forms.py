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
        fields = ['school_type', 'school', 'session_name', 'start_date', 'end_date']

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
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    
    class Meta:
        model = Term
        fields = ['academic_session', 'term_name', 'start_date', 'end_date']

    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__(*args, **kwargs)
        today = date.today()
        self.fields['academic_session'].queryset = AcademicSession.objects.filter(end_date__gte=today)

    def clean(self):
        cleaned_data = super().clean()
        academic_session = cleaned_data.get("academic_session")
        term_name = cleaned_data.get("term_name")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        instance = self.instance

        if academic_session is None:
            raise forms.ValidationError("Academic session is required.")

        if start_date is None or end_date is None:
            raise forms.ValidationError("Start date and end date are required.")

        # Validate term order and dates
        if term_name == '1':  # First Term
            if not (academic_session.start_date <= start_date <= end_date <= academic_session.end_date):
                raise forms.ValidationError("First term must start after the session start date and end before the session end date.")
        elif term_name == '2':  # Second Term
            first_term = Term.objects.filter(academic_session=academic_session, term_name='1').first()
            if not first_term:
                raise forms.ValidationError("First term must be set before the second term.")
            if not (first_term.end_date < start_date <= end_date <= academic_session.end_date):
                raise forms.ValidationError("Second term must start after the first term ends and end before the session end date.")
        elif term_name == '3':  # Third Term
            second_term = Term.objects.filter(academic_session=academic_session, term_name='2').first()
            if not second_term:
                raise forms.ValidationError("Second term must be set before the third term.")
            if not (second_term.end_date < start_date <= end_date <= academic_session.end_date):
                raise forms.ValidationError("Third term must start after the second term ends and end before the session end date.")

        # Ensure term is not duplicated, exclude the current instance if updating
        if Term.objects.filter(academic_session=academic_session, term_name=term_name).exclude(pk=instance.pk).exists():
            raise forms.ValidationError(f"The {self.fields['term_name'].choices[int(term_name) - 1][1]} for this academic session has already been set.") # type: ignore

        today = date.today()
        if academic_session.end_date < today:
            raise forms.ValidationError("The term cannot be set for a past academic session.")

        return cleaned_data

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name', 'program', 'is_general', 'school']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SubjectForm, self).__init__(*args, **kwargs)
        
        if user and user.is_ministry_admin:
            self.fields['school'].queryset = School.objects.all()
        elif user and user.is_school_admin:
            self.fields['school'].queryset = School.objects.filter(id=user.school_id)
            self.fields['is_general'].widget = forms.HiddenInput()
            self.fields['school'].initial = user.school
            self.fields['school'].widget = forms.HiddenInput()
