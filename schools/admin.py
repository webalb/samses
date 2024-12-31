from django.contrib import admin
from .models import AcademicSession, Term, School, SubjectRepository as Subject

class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'school_type', 'program', 'start_date', 'end_date', 'school')
    list_filter = ('school_type', 'program', 'school')
    search_fields = ('session_name', 'school__name')
    

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'name', 'school_type', 'program', 'logo')
    list_filter = ('school_type',)
    search_fields = ('name',)

    # Add custom form field for "Generate" button
    class Media:
        js = ('js/school_admin.js',)  # Link to external JS file


# Registering the models with their corresponding admin classes
admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(School, SchoolAdmin)
