from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile



admin.site.register(CustomUser, UserAdmin)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo']
    raw_id_fields = ['user']