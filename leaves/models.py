from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Leave(models.Model):
    LEAVE_TYPES = [
        ('PTO', _('Fizetett szabadság (PTO)')),
        ('SIC', _('Betegszabadság (Táppénz)')),
        ('UNP', _('Fizetés nélküli szabadság')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaves', verbose_name=_('Felhasználó'))
    start_date = models.DateField(verbose_name=_('Kezdés dátuma'))
    end_date = models.DateField(verbose_name=_('Befejezés dátuma'))
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES, default='PTO', verbose_name=_('Típus'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Megjegyzés'))

    def __str__(self):
        return f"{self.user.username} - {self.get_leave_type_display()} ({self.start_date} -> {self.end_date})"

    def clean(self):
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError({'end_date': 'A befejező dátum nem lehet korábbi a kezdő dátumnál.'})

    def save(self, *args, **kwargs):
        """Felülírjuk a save metódust, hogy a validáció minden mentésnél lefusson."""
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Leave'
        verbose_name_plural = 'Leaves'
        ordering = ['-start_date']
