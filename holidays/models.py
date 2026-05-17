from django.db import models
from django.utils.translation import gettext_lazy as _

class Holiday(models.Model):
    date = models.DateField(unique=True, verbose_name=_("Date"))
    description = models.CharField(max_length=200, verbose_name=_("Description"))
    is_working_day = models.BooleanField(
        default=False, 
        verbose_name=_("Working Day Exception"), 
        help_text=_("Check if this is a relocated working day (e.g. a working Saturday).")
    )

    class Meta:
        verbose_name = _("Holiday")
        verbose_name_plural = _("Holidays")
        ordering = ['date']

    def __str__(self):
        return f"{self.date} - {self.description}"

