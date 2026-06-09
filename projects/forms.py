from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import Project
from clients.models import Client

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'name', 'calendar', 'assigned_users', 'max_daily_hours', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'client': forms.Select(attrs={'class': 'tom-select'}),
            'calendar': forms.Select(attrs={'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-brand focus:border-brand sm:text-sm rounded-md'}),
            'assigned_users': forms.SelectMultiple(attrs={'class': 'tom-select-multiple'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.fields['assigned_users'].queryset = User.objects.filter(is_active=True, is_staff=False, is_superuser=False).order_by('last_name', 'first_name')

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name) < 5:
            raise ValidationError(_('A projekt nevének legalább 5 karakter hosszúnak kell lennie.'))
        return name
