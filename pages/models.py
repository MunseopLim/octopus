from django.db import models

# Create your models here.
class ResourceEntry(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    ip = models.CharField(max_length=30)
    connected = models.BooleanField()
    def __str__(self):
        return f'Emaillist({self.name})'