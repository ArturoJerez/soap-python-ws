from django.db import models

class Ubicacion(models.Model):
    centro = models.DecimalField(max_length=9, unique=True, blank=True, null=True)
    nivel1 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    nivel2 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    nivel3 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    nivel4 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    nivel5 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    nivel6 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'
        default_permissions = ()
        
    def __str__(self):
        return self.centro