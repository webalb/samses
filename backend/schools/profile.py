from django.core.management.base import BaseCommand
import cProfile
import pstats
from django.core.management import setup_environ
import os

# Find the path to your Django project settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')  # Replace 'your_project_name' with your actual project name

# Setup Django environment
setup_environ() 

from .models import School 

class Command(BaseCommand):
    help = 'Profile the execution of specific School model methods.'

    def handle(self, *args, **options):
        school = School.objects.first()  # Replace with your actual data

        methods_to_profile = [
            "get_academic_session",
            "status",
            "get_levels_and_classes",
        ]

        for method_name in methods_to_profile:
            self.stdout.write(f"\nProfiling {method_name}...")
            profiler = cProfile.Profile()
            profiler.enable()
            getattr(school, method_name)()
            profiler.disable()

            stats = pstats.Stats(profiler)
            stats.sort_stats('cumulative')
            stats.print_stats()