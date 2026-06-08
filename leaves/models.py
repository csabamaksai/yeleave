from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from holidays.models import Holiday

class Leave(models.Model):
    LEAVE_TYPES = [
        ('PTO', _('Fizetett Szabadság')),
        ('SIC', _('Betegszabadság')),
        ('UNP', _('Fizetés Nélküli Szabadság')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaves', verbose_name=_('Tanácsadó'))
    start_date = models.DateField(verbose_name=_('Kezdés dátuma'))
    end_date = models.DateField(verbose_name=_('Befejezés dátuma'))
    leave_type = models.CharField(max_length=3, choices=LEAVE_TYPES, default='PTO', verbose_name=_('Típus'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Megjegyzés'))

    def __str__(self):
        return f"{self.user.username} - {self.get_leave_type_display()} ({self.start_date} -> {self.end_date})"

    def get_working_days(self):
        """Kiszámolja a tényleges munkanapok számát az intervallumban (hétvégék és ünnepek kivételével)."""
        if not self.start_date or not self.end_date:
            return 0
            
        curr = self.start_date
        working_days = 0
        holidays = Holiday.objects.filter(date__gte=self.start_date, date__lte=self.end_date)
        holiday_dict = {h.date: h for h in holidays}
        
        while curr <= self.end_date:
            is_weekend = curr.weekday() >= 5
            if curr in holiday_dict:
                if holiday_dict[curr].is_working_day:
                    working_days += 1
            else:
                if not is_weekend:
                    working_days += 1
            curr += timedelta(days=1)
            
        return working_days

    def clean(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError({'end_date': _('A befejező dátum nem lehet korábbi a kezdő dátumnál.')})
            
            # Ellenőrizzük, hogy a kezdő vagy a végdátum esik-e hétvégére/ünnepnapra
            def is_day_off(d):
                is_weekend = d.weekday() >= 5
                h = Holiday.objects.filter(date=d).first()
                if h:
                    if h.is_working_day:
                        return False
                    else:
                        return True
                return is_weekend

            if is_day_off(self.start_date):
                raise ValidationError({'start_date': _('A kezdő dátum nem eshet hétvégére vagy ünnepnapra.')})
            if is_day_off(self.end_date):
                raise ValidationError({'end_date': _('A befejező dátum nem eshet hétvégére vagy ünnepnapra.')})

            if self.get_working_days() == 0:
                raise ValidationError({'start_date': _('A megadott intervallum nem tartalmaz munkanapot.')})

    def save(self, *args, **kwargs):
        """Felülírjuk a save metódust, hogy a validáció minden mentésnél lefusson."""
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Szabadság')
        verbose_name_plural = _('Szabadságok')
        ordering = ['-start_date']
