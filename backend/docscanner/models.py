from django.db import models

# Create your models here.
from django.utils import timezone


class Group(models.Model):
    name = models.CharField(max_length=120)
    docList = models.CharField(max_length=120)

    def _str_(self):
        return self.name

    @classmethod
    def create(cls, name):
        group = cls(name=name)
        return group


class Document(models.Model):
    name = models.CharField(max_length=120)
    filePath = models.CharField(max_length=500)
    scanningDate = models.DateTimeField(default=timezone.now)
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
