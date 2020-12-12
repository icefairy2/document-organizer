# Create your views here.
import os
import cv2
from .serializers import DocumentSerializer
from .models import Document
from django.http.response import StreamingHttpResponse, HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from docscanner.camera import VideoCamera
from datetime import datetime
from rest_framework.response import Response

from backend import settings

camera = VideoCamera()


@api_view(['GET'])
def document_list(request):
    if request.method == 'GET':
        documents = Document.objects.all()

        documents_serializer = DocumentSerializer(documents, many=True)
        return JsonResponse(documents_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def document(request, file=''):
    if request.method == 'GET':
        image_data = open(file, "rb").read()
        return HttpResponse(image_data, content_type="image/jpg")

    elif request.method == 'POST':
        frame = camera.get_cv_frame()

        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_name = 'doc_' + dt_string + '.jpg'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        file_date = dt_string

        cv2.imwrite(file_path, frame)

        db_document = Document(name=file_name, filePath=file_path, scanningDate=file_date)
        db_document.save()

        serializer = DocumentSerializer(db_document)
        return HttpResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # TODO
        Document.objects.get(name=file).delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def rename_document(request):
    if request.method == 'POST':
        doc_id = request.data['id']
        file_name = request.data['new_name']

        db_document = Document.objects.get(id=doc_id)

        if db_document is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        old_file_path = db_document.filePath
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        os.rename(old_file_path, file_path)

        db_document.name = file_name
        db_document.filePath = file_path
        db_document.save()

        return HttpResponse(status=status.HTTP_200_OK)


def gen():
    while True:
        frame = camera.get_cv_frame()
        if frame is None:
            continue

        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            continue

        #encoded_frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + bytearray(jpeg) + b'\r\n\r\n')


# def camera_feed(request):
#     return StreamingHttpResponse(gen(),
#                                  content_type='multipart/x-mixed-replace; boundary=frame')
@api_view(['GET'])
def camera_feed(self):
    return Response(gen(), content_type='multipart/x-mixed-replace; boundary=frame')