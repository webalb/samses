from django.contrib import admin
from .models import AcademicSession, Term, School, Subject

class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'school_type', 'program', 'start_date', 'end_date', 'school')
    list_filter = ('school_type', 'program', 'school')
    search_fields = ('session_name', 'school__name')

class TermAdmin(admin.ModelAdmin):
    list_display = ('academic_session', 'first_term', 'second_term', 'third_term')
    list_filter = ('academic_session',)
    search_fields = ('academic_session__session_name',)
    
    def first_term(self, obj):
        return f"{obj.start_date_1} - {obj.end_date_1}"
    first_term.short_description = 'First Term'

    def second_term(self, obj):
        return f"{obj.start_date_2} - {obj.end_date_2}"
    second_term.short_description = 'Second Term'

    def third_term(self, obj):
        return f"{obj.start_date_3} - {obj.end_date_3}"
    third_term.short_description = 'Third Term'

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'name', 'school_type', 'program', 'logo')
    list_filter = ('school_type',)
    search_fields = ('name',)

    # Add custom form field for "Generate" button
    class Media:
        js = ('js/school_admin.js',)  # Link to external JS file

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'program', 'is_general', 'is_optional', 'school')
    list_filter = ('program', 'is_general', 'is_optional', 'school')
    search_fields = ('subject_name', 'school__name')

# Registering the models with their corresponding admin classes
admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(Term, TermAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Subject, SubjectAdmin)
