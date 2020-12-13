import os
from datetime import datetime


from django.db import models

# Create your models here.
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=120)

    def _str_(self):
        return self.name

    @classmethod
    def create(cls, name):
        group = cls(name=name)
        return group

def upload_document_path(instance, filename):
    return os.path.join('/scanned_documents/', instance.document_id, filename)

class Document(models.Model):
    name = models.CharField(max_length=120)
    filePath = models.CharField(max_length=500)
    scanningDate = models.DateTimeField(default=datetime.now())
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="document_group",
        default=None,
        null=True
    )
    order = models.PositiveIntegerField(default=0)

    def _str_(self):
        return self.name
