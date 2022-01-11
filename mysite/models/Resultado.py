from django.db import models

class Resultado(models.Model):
    type = models.TextField(max_length=15, unique=True, blank=True, null=True)
    code = models.DecimalField(max_length=9, unique=True, blank=True, null=True)
    message = models.TextField(max_length=15, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Resultado'
        verbose_name_plural = 'Resultados'
        default_permissions = ()
        
    def __str__(self):
        return self.type