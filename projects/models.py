from django.db import models
from django.conf import settings
from clients.models import Client
from django.utils.translation import gettext_lazy as _

class Project(models.Model):
    CALENDAR_CHOICES = [
        ('hu', _('Magyar')),
        ('at', _('Osztrák')),
    ]
    
    name = models.CharField(max_length=255, verbose_name=_('Projekt Név'))
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects', verbose_name=_('Partner'))
    
    calendar = models.CharField(
        max_length=2, 
        choices=CALENDAR_CHOICES, 
        default='hu', 
        verbose_name=_('Naptár / Ország'),
        help_text=_('A projekt munkaszüneti napjait és munkarendjét határozza meg.')
    )
    
    max_daily_hours = models.IntegerField(default=8, verbose_name=_('Max napi könyvelhető óraszám'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Leírás'))
    
    # ManyToMany kapcsolat a felhasználókkal (kik vannak delegálva a projektre)
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='assigned_projects', 
        blank=True, 
        verbose_name=_('Hozzárendelt tanácsadók')
    )
    
    is_active = models.BooleanField(default=True, verbose_name=_('Aktív'))
    end_date = models.DateField(blank=True, null=True, verbose_name=_('Befejezés Dátuma'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Létrehozva'))

    def __str__(self):
        return f"{self.client.name} - {self.name}"

    class Meta:
        verbose_name = _('Projekt')
        verbose_name_plural = _('Projektek')
        ordering = ['client__name', 'name']
