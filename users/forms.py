from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserForm(forms.ModelForm):
    # Optional explicitly typed password field for new users
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label=_("Password")
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label=_("Confirm Password")
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        labels = {
            'username': _('Username'),
            'email': _('Email Address'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'is_active': _('Active'),
            'is_staff': _('Administrator (Staff)')
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password != password_confirm:
            raise ValidationError({
                "password_confirm": _("A két jelszó nem egyezik meg! Kérlek, próbáld újra.")
            })

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
