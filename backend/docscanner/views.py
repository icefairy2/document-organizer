from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
import cv2
from .serializers import DocumentSerializer
from .models import Document
from django.http.response import StreamingHttpResponse, HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from docscanner.camera import VideoCamera

camera = VideoCamera()


@api_view(['GET'])
def document_list(request):
    if request.method == 'GET':
        documents = Document.objects.all()

        documents_serializer = DocumentSerializer(documents, many=True)
        return JsonResponse(documents_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def document(request):
    if request.method == 'GET':
        # TODO
        return JsonResponse(status=status.HTTP_404_NOT_FOUND)
        # 'safe=False' for objects serialization

    elif request.method == 'POST':
        frame = camera.get_cv_frame()
        cv2.imwrite('test.jpg', frame)
        return HttpResponse(status=status.HTTP_200_OK)


def gen():
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def camera_feed(request):
    return StreamingHttpResponse(gen(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
