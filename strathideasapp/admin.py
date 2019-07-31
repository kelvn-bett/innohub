from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Ideas

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'gender', 'department', 'phone_number']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Ideas)

admin.site.site_header = 'InnoHub Administration'
