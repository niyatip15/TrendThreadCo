from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('email','first_name', 'last_name', 'last_login','is_active')
    list_display_links = ('first_name','last_name')
    readonly_fields = ('last_login',)
    ordering = ('email',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
admin.site.register(CustomUser,CustomUserAdmin)
