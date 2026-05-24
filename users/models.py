from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    is_reporter = models.BooleanField(
        _('Lekérdező'),
        default=False,
        help_text=_('Designates whether the user can access reports but not admin features.')
    )

    def __str__(self):
        return self.username
