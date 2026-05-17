from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'country', 'zip_code', 'city', 'address', 'contact_name', 'contact_phone']
        widgets = {
            'country': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
