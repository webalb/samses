from django import forms
from backend.schools.models import FeeStructure

class FeeStructureForm(forms.ModelForm):
    class Meta:
        model = FeeStructure
        fields = ['class_level', 'fee_type','is_optional', 'amount', 'description']
        widgets = {
            'class_level': forms.Select(attrs={'class': 'form-control'}),
            'fee_type': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_optional': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
