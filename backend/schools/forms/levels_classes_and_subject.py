from django import forms
from backend.schools.models import LevelClasses, ProgramLevelTemplate, Stream, SubjectRepository, SchoolSubject

class LevelClassesForm(forms.ModelForm):
    class Meta:
        model = LevelClasses
        fields = ['program_level_template', 'class_section_name', 'stream', 'capacity']

    def __init__(self, *args, **kwargs):
        program_level_template = kwargs.pop('program_level_template', None)  # Get program level from kwargs
        super().__init__(*args, **kwargs)

        # Dynamically filter the queryset for the stream field
        if program_level_template and 'stream' in self.fields:
            self.fields['stream'].queryset = Stream.objects.filter(program_level_template=program_level_template)

        # Add Bootstrap CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        """
        Perform any additional validation here if needed.
        """
        cleaned_data = super().clean()
        program_level_template = cleaned_data.get('program_level_template')
        stream = cleaned_data.get('stream')

        # Ensure stream belongs to the selected program level template
        if stream and program_level_template and stream.program_level_template != program_level_template:
            raise forms.ValidationError({
                'stream': 'Selected stream does not belong to the chosen program level.'
            })

        return cleaned_data


class ClassWithoutProgramLevelFieldForm(LevelClassesForm):
    class Meta(LevelClassesForm.Meta):
        exclude = ['program_level_template']


class NoStreamForm(LevelClassesForm):
    class Meta(LevelClassesForm.Meta):
        exclude = ['program_level_template', 'stream']






class SubjectRepositoryForm(forms.ModelForm):
    class Meta:
        model = SubjectRepository
        fields = ['subject_name', 'category', 'vocational_department', 'description', 'program_levels', 'streams']
        widgets = {
            'program_levels': forms.CheckboxSelectMultiple(),
            'streams': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in ['program_levels', 'streams']:
                field.widget.attrs['class'] = ''
            else:
                field.widget.attrs['class'] = 'form-control'



from django import forms
from backend.schools.models import SchoolSubject, SubjectRepository

class SchoolSubjectForm(forms.ModelForm):
    class Meta:
        model = SchoolSubject
        fields = ['subject_repository', 'is_compulsory', 'is_active']
        widgets = {
            'subject_repository': forms.Select(attrs={'class': 'form-control'}),
            'is_compulsory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'subject_repository': 'Subject',
            'is_compulsory': 'Is this subject compulsory?',
            'is_active': 'Is this subject active?',
        }

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)  # School instance passed during form initialization
        super().__init__(*args, **kwargs)

        from django.db.models import Q

        if school:
            # Split the school's program into components (e.g., 'jss+sss' -> ['jss', 'sss'])
            program_components = school.program.split('+')

            # Fetch related DepartmentRepository objects from SchoolDepartment
            school_departments = school.school_departments.values_list('departments', flat=True)

            # Fetch subjects already linked to the school
            existing_subjects = school.offered_subjects.values_list('subject_repository', flat=True)

            # Query the SubjectRepository for subjects matching the school's program components
            self.fields['subject_repository'].queryset = SubjectRepository.objects.filter(
                Q(category__in=['core', 'religious', 'local_language']) |  # Non-vocational subjects
                Q(
                    category='vocational',
                    vocational_department__id__in=school_departments  # Vocational subjects limited to selected departments
                )
            ).filter(
                program_levels__program__in=program_components
            ).exclude(id__in=existing_subjects).distinct()

        # Add a prompt for the subject selection dropdown
        self.fields['subject_repository'].empty_label = 'Select a subject'

