from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

admin.site.register(CustomUser)

# class CustomUserAdmin(UserAdmin):
#     list_display = (
#         'email','fname','lastname','gender','Date_Of_Birth','country','Profession',
#         )

# admin.site.register(CustomUser, CustomUserAdmin)    


