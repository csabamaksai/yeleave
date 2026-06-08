from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Leave

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'leave_type', 'notes']
        labels = {
            'start_date': _('Kezdés dátuma'),
            'end_date': _('Befejezés dátuma'),
            'leave_type': _('Típus'),
            'notes': _('Megjegyzés'),
        }
        widgets = {
            'start_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-brand focus:border-brand sm:text-sm'}),
            'end_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-brand focus:border-brand sm:text-sm'}),
            'leave_type': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-brand focus:border-brand sm:text-sm'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-brand focus:border-brand sm:text-sm'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            from datetime import date
            today = date.today()
            
            # Start date limit check
            start_limit = date(start_date.year, start_date.month, 20)
            if today > start_limit:
                self.add_error('start_date', _("Erre a hónapra már nem rögzíthetsz szabadságot, mivel a hónap 20-a elmúlt."))
                
            # End date limit check if different month
            if start_date.month != end_date.month or start_date.year != end_date.year:
                end_limit = date(end_date.year, end_date.month, 20)
                if today > end_limit:
                    self.add_error('end_date', _("A befejezés hónapjára már nem rögzíthetsz szabadságot, mivel a hónap 20-a elmúlt."))

        return cleaned_data
