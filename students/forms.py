# from django import forms
# from .models import Student

# class StudentForm(forms.ModelForm):
#     class Meta:
#         model = Student
#         exclude = ['admission_number']  # Exclude admission_number from user input
#         widgets = {
#             'passport_photograph': forms.FileInput(attrs={'accept': 'image/*'}),  # Customize widget for passport_photograph
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'})  # Customize widget for date_of_birth
#         }
