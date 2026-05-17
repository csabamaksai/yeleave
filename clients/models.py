from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Név')
    country = models.CharField(max_length=100, default='Magyarország', verbose_name='Ország')
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Irányítószám')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Város')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Cím (utca, házszám)')
    
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Kapcsolattartó neve')
    contact_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Kapcsolattartó telefon')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Létrehozva')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['name']
