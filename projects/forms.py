from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import Project
from clients.models import Client

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['client', 'name', 'assigned_users', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'client': forms.Select(attrs={'class': 'tom-select'}),
            'assigned_users': forms.SelectMultiple(attrs={'class': 'tom-select-multiple'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name) < 5:
            raise ValidationError(_('A projekt nevének legalább 5 karakter hosszúnak kell lennie.'))
        return name
