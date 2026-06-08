from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    EMPLOYMENT_TYPE_CHOICES = [
        ('employee', _('Alkalmazott')),
        ('contractor', _('Vállalkozó')),
    ]
    employment_type = models.CharField(
        _('Jogviszony'),
        max_length=20,
        choices=EMPLOYMENT_TYPE_CHOICES,
        default='contractor',
    )
    annual_leave_allowance = models.IntegerField(
        _('Éves szabadságkeret (nap)'),
        null=True,
        blank=True,
        help_text=_('Csak alkalmazott esetén értelmezett.')
    )

    is_company_admin = models.BooleanField(
        _('Cégvezető / Admin'),
        default=False,
        help_text=_('A felületen minden funkcióhoz hozzáfér (Projektek, Partnerek, Felhasználók stb.), de nem Django site admin.')
    )
    is_reporter = models.BooleanField(
        _('Lekérdező (Könyvelő)'),
        default=False,
        help_text=_('Csak a riportokhoz fér hozzá.')
    )

    def __str__(self):
        return self.username
