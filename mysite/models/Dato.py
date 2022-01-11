from django.db import models

class Dato(models.Model):
    descripcion = models.TextField(max_length=15, unique=True, blank=True, null=True)
    codigo = models.TextField(max_length=9, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Dato'
        verbose_name_plural = 'Datos'
        default_permissions = ()
        
    def __str__(self):
        return self.descripcion