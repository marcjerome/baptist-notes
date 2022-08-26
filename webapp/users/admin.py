# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Details', {'fields': ('first_name', 'middle_name', 'last_name')}),
        ('Additional Profile', {'fields': ('bio',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})    
    )

    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields': ('username','email', 'password1', 'password2'),
        }),
    )

    
    
admin.site.register(CustomUser, CustomUserAdmin)