from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserForm(forms.ModelForm):
    ROLE_CHOICES = (
        ('user', _('Normál felhasználó')),
        ('reporter', _('Lekérdező (Könyvelő/Asszisztens)')),
        ('admin', _('Adminisztrátor')),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label=_('Felhasználói jogosultság'),
        initial='user',
        required=True
    )

    # Optional explicitly typed password field for new users
    password = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label=_("Jelszó")
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(), 
        required=False, 
        label=_("Jelszó újra")
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'employment_type', 'annual_leave_allowance']
        labels = {
            'username': _('Felhasználónév'),
            'email': _('Email cím'),
            'first_name': _('Keresztnév'),
            'last_name': _('Vezetéknév'),
            'is_active': _('Aktív'),
            'employment_type': _('Jogviszony'),
            'annual_leave_allowance': _('Éves szabadságkeret (nap)'),
        }
        widgets = {
            'email': forms.EmailInput(attrs={'type': 'email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
        # Ha a felhasználó létezik, beállítjuk a role mező kezdőértékét
        if self.instance.pk:
            if getattr(self.instance, 'is_company_admin', False) or self.instance.is_superuser or self.instance.is_staff:
                self.fields['role'].initial = 'admin'
            elif getattr(self.instance, 'is_reporter', False):
                self.fields['role'].initial = 'reporter'
            else:
                self.fields['role'].initial = 'user'
        else:
            # Ha új felhasználót hozunk létre, a jelszó mezők kötelezők
            self.fields['password'].required = True
            self.fields['password_confirm'].required = True

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password:
            if len(password) < 8:
                raise ValidationError(_("A jelszónak legalább 8 karakter hosszúnak kell lennie."))
            if not any(char.isalpha() for char in password):
                raise ValidationError(_("A jelszónak tartalmaznia kell legalább egy betűt."))
            if not any(char.isdigit() for char in password):
                raise ValidationError(_("A jelszónak tartalmaznia kell legalább egy számot."))
            if not any(not char.isalnum() for char in password):
                raise ValidationError(_("A jelszónak tartalmaznia kell legalább egy speciális karaktert."))
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        employment_type = cleaned_data.get("employment_type")
        annual_leave_allowance = cleaned_data.get("annual_leave_allowance")

        if password and password != password_confirm:
            raise ValidationError({
                "password_confirm": _("A két jelszó nem egyezik meg! Kérlek, próbáld újra.")
            })
            
        if employment_type == 'employee' and annual_leave_allowance is None:
            self.add_error('annual_leave_allowance', _("Alkalmazott esetén kötelező megadni az éves szabadságkeretet."))
            
        if employment_type != 'employee':
            cleaned_data['annual_leave_allowance'] = None

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        role = self.cleaned_data.get('role')
        if role == 'admin':
            user.is_company_admin = True
            user.is_reporter = False
            user.is_staff = False  # Ezt levesszük, ne legyen automatikus Django admin hozzáférése
            user.is_superuser = False
        elif role == 'reporter':
            user.is_company_admin = False
            user.is_reporter = True
            user.is_staff = False
            user.is_superuser = False
        else:
            user.is_company_admin = False
            user.is_reporter = False
            user.is_staff = False
            user.is_superuser = False
            
        if commit:
            user.save()
        return user
