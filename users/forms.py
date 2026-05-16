from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):
    # Optional explicitly typed password field for new users
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Jelszó")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']
        labels = {
            'username': 'Felhasználónév',
            'email': 'E-mail cím',
            'first_name': 'Keresztnév',
            'last_name': 'Vezetéknév',
            'is_active': 'Aktív',
            'is_staff': 'Cégvezető (Admin)'
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
