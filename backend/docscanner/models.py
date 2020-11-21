from django.db import models


# Create your models here.


class Document(models.Model):
    name = models.CharField(max_length=120)
    filePath = models.CharField(max_length=500)

    def _str_(self):
        return self.name
