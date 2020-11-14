from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import DocumentSerializer
from .models import Document
from rest_framework.views import APIView
from rest_framework.response import Response


class DocumentView(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def post(self, request):
        document_data = request.data
        new_document = Document.objects.create(name = document_data["name"], filePath = document_data["filePath"])
        new_document.save()
        serializer = DocumentSerializer(new_document)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATE)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        self.perform_destroy(document)
        return Response(status=status.HTTP_204_NO_CONTENT)

