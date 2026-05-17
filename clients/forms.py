from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'contract_number', 'country', 'zip_code', 'city', 'address', 'contact_name', 'contact_phone']
        widgets = {
            'country': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name or len(name) < 5:
            raise ValidationError(_('A névnek legalább 5 karakter hosszúnak kell lennie.'))
        return name
