from django.db import models


# Create your models here.
from django.utils import timezone


class Document(models.Model):
    name = models.CharField(max_length=120)
    filePath = models.CharField(max_length=500)
    scanningDate = models.DateTimeField(default=timezone.now)

    def _str_(self):
        return self.name
