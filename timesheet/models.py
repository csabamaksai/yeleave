from django.db import models
from django.conf import settings
from projects.models import Project
from django.utils.translation import gettext_lazy as _

class TimeEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='time_entries', verbose_name=_('Dolgozó'))
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='time_entries', verbose_name=_('Projekt'))
    date = models.DateField(verbose_name=_('Dátum'))
    
    # Mennyi időt dolgozott (órában megadva, pl. 4.5 = négy és fél óra)
    hours = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_('Órák'))
    
    description = models.TextField(blank=True, null=True, verbose_name=_('Leírás'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.name} - {self.date} ({self.hours}h)"

    class Meta:
        verbose_name = _('Munkaóra')
        verbose_name_plural = _('Munkaórák')
        # Nagyon fontos: ne lehessen ugyanarra a napra, ugyanarra a projektre két KÜLÖN bejegyzést csinálni egy embernek.
        # Inkább egy bejegyzés legyen, összeadott órákkal (ahogy a Tempóban is egy cella van egy napra)
        unique_together = [['user', 'project', 'date']]
        ordering = ['-date', 'project__name']


class ClientCertificate(models.Model):
    UNIT_CHOICES = [
        ('days', _('Nap')),
        ('hours', _('Óra')),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_certificates', verbose_name=_('Felhasználó'))
    client = models.ForeignKey('clients.Client', on_delete=models.CASCADE, related_name='client_certificates', verbose_name=_('Partner'))
    year = models.IntegerField(verbose_name=_('Év'))
    month = models.IntegerField(verbose_name=_('Hónap'))
    value = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Érték'))
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='days', verbose_name=_('Mértékegység'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Megjegyzés'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Partner TIG')
        verbose_name_plural = _('Partner TIG-ek')
        unique_together = [['user', 'client', 'year', 'month']]

    def __str__(self):
        return f"{self.user} - {self.client} - {self.year}/{self.month} ({self.value} {self.get_unit_display()})"
