from django import forms
from backend.schools.models import School
from django.forms.widgets import Select
from django.utils.html import escape
from itertools import groupby


PROGRAM_CHOICES = [
    ('primary', 'Primary'),
    ('jss', 'Junior Secondary School'),
    ('sss', 'Senior Secondary School'),
]
class SelectSchoolForm(forms.Form):
    school = forms.ModelChoiceField(
        queryset=School.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control select2'}),
        help_text="Select the school for which you want to set the enrollment details."
    )

class SetProgramForm(forms.Form):
    program = forms.ChoiceField(
        choices=[],  # Choices will be populated dynamically in the view
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the program offered by the school."
    )

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            if school.PROGRAM_CHOICES == 'all':
                self.fields['program'].choices = PROGRAM_CHOICES
            else:
                self.fields['program'].choices = [
                    (choice[0], choice[1]) for choice in School.PROGRAM_CHOICES if choice[0] in school.program.split('+')
                ]


from backend.schools.models import ProgramLevelTemplate, Stream, LevelClasses

class SetProgramLevelStreamForm(forms.Form):
    program_level = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the program level for enrollment."
    )
    stream = forms.ChoiceField(
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the stream if applicable (only for SSS programs)."
    )

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)

        self.fields['program_level'].choices = self._get_program_level_choices(school, program)

        if school and program:
            if program == 'sss':  # Streams only applicable for SSS programs
                self.fields['stream'].choices = self._get_stream_choices(program)

    def _get_program_level_choices(self, school, program):
        choices = []
        if school and program:
            level_and_classes = LevelClasses.objects.filter(school=school, program_level_template__program=program)
            for level, level_classes in groupby(level_and_classes, lambda obj: obj.program_level_template.level):
                group_label = escape(level)
                group_choices = [(obj.id, f"{obj.program_level_template.level} - {obj.class_section_name}") for obj in level_classes]
                print(group_choices)
                choices.append((group_label, group_choices))
        return choices
    def _get_stream_choices(self, program):
        choices = []
        streams = Stream.objects.filter(program_level_template__program=program)
        for level, stream in groupby(streams, lambda obj: obj.program_level_template.level):
                group_label = escape(level)
                group_choices = [(obj.id, obj.name) for obj in stream]
                choices.append((group_label, group_choices))
        return choices

from backend.student.models import EnrollmentRecord

class EnrollmentFinalForm(forms.ModelForm):
    class Meta:
        model = EnrollmentRecord
        fields = ['enrollment_mode', 'generate_admission_info', 'is_active']
        widgets = {
            'enrollment_mode': forms.Select(attrs={'class': 'form-control'}),
            'generate_admission_info': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class EnrollmentRecordForm(forms.ModelForm):
    class Meta:
        model = EnrollmentRecord
        fields = ['school', 'program', 'program_level', 'stream', 'enrollment_mode', 'is_active']
        widgets = {
            'school': forms.Select(attrs={'class': 'form-control'}),
            'program': forms.TextInput(attrs={'class': 'form-control'}),
            'program_level': forms.Select(attrs={'class': 'form-control'}),
            'stream': forms.Select(attrs={'class': 'form-control'}),
            'enrollment_mode': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
