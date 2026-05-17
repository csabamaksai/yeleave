from django import forms
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
