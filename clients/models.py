from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name')
    address = models.TextField(blank=True, null=True, verbose_name='Address')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        ordering = ['name']
