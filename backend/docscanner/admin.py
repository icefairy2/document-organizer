from django.contrib import admin
# Register your models here.
from .models import Document
from .models import Group


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'filePath', 'scanningDate', 'group')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Register your models here.
admin.site.register(Document, DocumentAdmin)
admin.site.register(Group, GroupAdmin)
