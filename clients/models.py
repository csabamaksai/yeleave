from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    country = models.CharField(max_length=100, default='Hungary', verbose_name='Country')
    zip_code = models.CharField(max_length=20, blank=True, null=True, verbose_name='Zip Code')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='City')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Address')
    
    contact_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Contact Name')
    contact_phone = models.CharField(max_length=50, blank=True, null=True, verbose_name='Contact Phone')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['name']
