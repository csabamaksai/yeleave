from django.contrib import admin
from .models import Holiday

@admin.register(Holiday)
class HolidayAdmin(admin.ModelAdmin):
    list_display = ('date', 'description', 'is_working_day')
    list_filter = ('is_working_day', 'date')
    search_fields = ('description',)
    date_hierarchy = 'date'

