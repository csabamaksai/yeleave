from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_company_admin', 'is_reporter', 'is_staff', 'is_active']

    fieldsets = UserAdmin.fieldsets + (
        ('Egyedi jogosultságok', {'fields': ('is_company_admin', 'is_reporter')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
