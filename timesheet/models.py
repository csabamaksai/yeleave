from django.db import models
from django.conf import settings
from projects.models import Project

class TimeEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='time_entries', verbose_name='User')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='time_entries', verbose_name='Project')
    date = models.DateField(verbose_name='Date')
    
    # Mennyi időt dolgozott (órában megadva, pl. 4.5 = négy és fél óra)
    hours = models.DecimalField(max_digits=4, decimal_places=2, verbose_name='Hours')
    
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.project.name} - {self.date} ({self.hours}h)"

    class Meta:
        verbose_name = 'Time Entry'
        verbose_name_plural = 'Time Entries'
        # Nagyon fontos: ne lehessen ugyanarra a napra, ugyanarra a projektre két KÜLÖN bejegyzést csinálni egy embernek.
        # Inkább egy bejegyzés legyen, összeadott órákkal (ahogy a Tempóban is egy cella van egy napra)
        unique_together = [['user', 'project', 'date']]
        ordering = ['-date', 'project__name']

