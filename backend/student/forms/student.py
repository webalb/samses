from datetime import date

from django import forms
from django.forms import DateInput
from django.core.validators import RegexValidator
from backend.student.models import Student, Guardian

class StudentForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Student
        exclude = [
            'id', 'school', 'is_active', 'created_at', 'updated_at', 'reg_num'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name not in ['']:
                field.widget.attrs['class'] = 'form-control'

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')

        # Calculate minimum allowed date of birth for a 4-year-old student
        today = date.today()
        min_allowed_dob = today.replace(year=today.year - 4)
        # Raise validation error if dob is less than the minimum allowed date
        if dob > min_allowed_dob:
            raise forms.ValidationError("Student must be at least 4 years old.")
        return dob


class GuardianForm(forms.ModelForm):
    class Meta:
        model = Guardian
        fields = ['full_name', 'relationship', 'role', 'phone_number', 'email', 'address']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
