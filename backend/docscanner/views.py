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
file_names = dict()


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

        # dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        number = file_names.get(file, 0)

        file_names[file] = number + 1

        file_name = 'doc_' + file + str(number) + '.jpg'

        file_path = os.path.join(settings.MEDIA_ROOT, file_name)

        cv2.imwrite(file_path, frame)

        db_document = Document(name=file_name, filePath=file_path)

        db_document.save()

        serializer = DocumentSerializer(data=db_document)

        if serializer.is_valid():
            serializer.save()

            return HttpResponse(serializer.data, status=status.HTTP_200_OK)

        return HttpResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # TODO
        Document.objects.get(name=file).delete()
        return Response(status=status.HTTP_200_OK)


def gen():
    while True:
        frame = camera.get_cv_frame()
        ret, jpeg = cv2.imencode('.jpg', frame)
        encoded_frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n\r\n')


def camera_feed(request):
    return StreamingHttpResponse(gen(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
