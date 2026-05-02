from django.db import models
from django.conf import settings
from clients.models import Client

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='Project Name')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects', verbose_name='Client')
    description = models.TextField(blank=True, null=True, verbose_name='Description')
    
    # ManyToMany kapcsolat a felhasználókkal (kik vannak delegálva a projektre)
    assigned_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='assigned_projects', 
        blank=True, 
        verbose_name='Assigned Users'
    )
    
    is_active = models.BooleanField(default=True, verbose_name='Active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} - {self.name}"

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'
        ordering = ['client__name', 'name']
