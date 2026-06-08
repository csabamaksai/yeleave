from django.db import models
from django.utils.translation import gettext_lazy as _

class Holiday(models.Model):
    date = models.DateField(unique=True, verbose_name=_("Dátum"))
    description = models.CharField(max_length=200, verbose_name=_("Leírás"))
    is_working_day = models.BooleanField(
        default=False, 
        verbose_name=_("Áthelyezett munkanap"), 
        help_text=_("Jelöld be, ha ez egy pihenőnapra eső áthelyezett munkanap (pl. munkanap szombat).")
    )

    class Meta:
        verbose_name = _("Ünnepnap / Pihenőnap")
        verbose_name_plural = _("Ünnepnapok / Pihenőnapok")
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.description}"

