from django import forms
from backend.schools.models import GradingScale, GradeBoundary, SubjectGradingConfiguration

class GradingScaleForm(forms.ModelForm):
    class Meta:
        model = GradingScale
        fields = ['scale_name', 'description']
        widgets = {
            'scale_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class GradeBoundaryForm(forms.ModelForm):
    class Meta:
        model = GradeBoundary
        fields = ['grading_scale', 'grade', 'lower_bound', 'upper_bound', 'description']
        widgets = {
            'grading_scale': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
            'lower_bound': forms.NumberInput(attrs={'class': 'form-control'}),
            'upper_bound': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class SubjectGradingConfigurationForm(forms.ModelForm):
    class Meta:
        model = SubjectGradingConfiguration
        fields = ['grading_scale', 'weightage']
        widgets = {
            'grading_scale': forms.Select(attrs={'class': 'form-control'}),
            'weightage': forms.NumberInput(attrs={'class': 'form-control'}),
        }
