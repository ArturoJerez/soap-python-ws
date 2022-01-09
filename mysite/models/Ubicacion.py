from django.db import models

class Ubicacion(models.Model):
    ubicacion = models.TextField(max_length=15, unique=True, blank=True, null=True)
    nivel1 = models.TextField(max_length=15, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Ubicacion'
        verbose_name_plural = 'Ubicaciones'
        default_permissions = ()
        
    def __str__(self):
        return self.ubicacion