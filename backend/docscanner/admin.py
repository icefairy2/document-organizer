from django.contrib import admin
# Register your models here.
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'filePath')


# Register your models here.
admin.site.register(Document, DocumentAdmin)
