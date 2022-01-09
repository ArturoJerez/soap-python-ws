from django.db import models

class Elemento(models.Model):
    elemento1 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    elemento2 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    elemento3 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Elemento'
        verbose_name_plural = 'Elementos'
        default_permissions = ()
        
    def __str__(self):
        return self.elemento1