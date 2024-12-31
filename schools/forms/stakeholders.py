from django import forms
from schools.models import Staff

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = [
            'full_name', 'position', 'email', 'phone_number', 'is_active',
            'date_joined', 'salary_amount', 'profile_picture'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_joined': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
