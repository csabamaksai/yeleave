from django.contrib import admin
from .models import TimeEntry

@admin.register(TimeEntry)
class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'date', 'hours', 'created_at')
    list_filter = ('project', 'date', 'user')
    search_fields = ('user__username', 'project__name', 'description')
    date_hierarchy = 'date'
