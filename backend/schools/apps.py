from django.db.models.signals import post_migrate
from django.apps import AppConfig
from django.core.management import call_command

class SchoolsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.schools'

#     def ready(self):
#         post_migrate.connect(load_fixtures, sender=self)

# def load_fixtures(sender, **kwargs):
#     from backend.schools.models import ProgramLevelTemplate
#     if ProgramLevelTemplate.objects.count() == 0:
#         call_command('loaddata', 'program_level_template.json')
