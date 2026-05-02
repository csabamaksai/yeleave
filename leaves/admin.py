from django.contrib import admin
from .models import Leave

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('user', 'leave_type', 'start_date', 'end_date')
    list_filter = ('leave_type', 'start_date', 'user')
    search_fields = ('user__username', 'notes')
    date_hierarchy = 'start_date'
