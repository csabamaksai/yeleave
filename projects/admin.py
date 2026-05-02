from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'is_active', 'created_at')
    list_filter = ('is_active', 'client')
    search_fields = ('name', 'client__name')
    # Ez csinál egy szép, dupla listás választót a userek delegálásához az adminban:
    filter_horizontal = ('assigned_users',)
