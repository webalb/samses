from django import forms
from backend.schools.models import SchoolFeedback

class SchoolFeedbackForm(forms.ModelForm):
    class Meta:
        model = SchoolFeedback
        fields = ['school', 'role', 'feedback_by', 'subject', 'feedback_text']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'feedback_by': forms.TextInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'feedback_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }
        labels = {
            'school': 'School',
            'role': 'Your Role',
            'feedback_by': 'Your Name (Optional)',
            'subject': 'Feedback Title',
            'feedback_text': 'Feedback Details',
        }
