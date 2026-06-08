from django.db import models
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=_('Név'))
    country = models.CharField(max_length=100, default='Hungary', verbose_name=_('Ország'))
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Irányítószám'))
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Város'))
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Cím'))
    contract_number = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Szerződésszám'))
    
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Kapcsolattartó neve'))
    contact_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('Kapcsolattartó telefonja'))
    
    is_active = models.BooleanField(default=True, verbose_name=_('Aktív'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Létrehozva'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Partner')
        verbose_name_plural = _('Partnerek')
        ordering = ['name']
