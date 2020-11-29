from django.contrib import admin
# Register your models here.
from .models import Document
from .models import Group

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'filePath', 'groupId')

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'docList')

# Register your models here.
admin.site.register(Document, DocumentAdmin)
admin.site.register(Group, GroupAdmin)
