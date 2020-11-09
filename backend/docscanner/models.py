from django.db import models


# Create your models here.


class Document(models.Model):
    name = models.CharField(max_length=120)
    filePath = models.FileField(upload_to='./test')

    def _str_(self):
        return self.name
