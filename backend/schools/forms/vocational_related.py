from django import forms
from backend.schools.models import  VocationalPartnership, DepartmentRepository, SchoolDepartment


class DepartmentRepositoryForm(forms.ModelForm):
    class Meta:
        model = DepartmentRepository
        fields = ['department', 'description', 'certification_awarded']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'certification_awarded': forms.TextInput(attrs={'class': 'form-control'}),

            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Department Name'}),
           
        }
        labels = {
            'department': 'Department Name',
            'description': 'Description',
            'certification_awarded': 'Certification Awarded',
        }

class SchoolDepartmentForm(forms.ModelForm):
    class Meta:
        model = SchoolDepartment
        fields = ['departments']
        widgets = {
            'departments': forms.Select(attrs={'class': 'form-control',}),

        }
        labels = {
            'departments': 'Select Department',
        }
    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)  # School instance passed during form initialization
        super().__init__(*args, **kwargs)

        if school:
         
            # Fetch subjects already linked to the school
            existing_departments = school.school_departments.values_list('departments', flat=True)

            # Query the SubjectRepository for subjects matching the school's program components
            self.fields['departments'].queryset = DepartmentRepository.objects.all().exclude(id__in=existing_departments)



class VocationalPartnershipForm(forms.ModelForm):
    class Meta:
        model = VocationalPartnership
        fields = [
            'partner_name', 
            'partnership_type', 
            'description', 
            'partner_address', 
            'start_date', 
            'end_date'
        ]
        widgets = {
            'school': forms.HiddenInput(),
            'partner_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Partner Name'}),
            'partnership_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Details of the partnership'}),
            'partner_address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Partner Address'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
