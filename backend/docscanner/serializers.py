from rest_framework import serializers
from .models import Document
from .models import Group

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'name', 'filePath', 'scanningDate', 'group', 'order')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')