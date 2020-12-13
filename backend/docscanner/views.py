# Create your views here.
import json
import os
import cv2
from .serializers import DocumentSerializer
from .serializers import GroupSerializer
from .models import Document
from .models import Group
from django.http.response import StreamingHttpResponse, HttpResponse
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from .camera import VideoCamera
from datetime import datetime
from rest_framework.response import Response

from backend import settings

camera = VideoCamera()


# method to update the document on merging
def update_document(db_document, group_id, order):
    db_document.group = group_id
    db_document.order = order
    db_document.save()


# method to get a list of documents in a group
def all_documents_in_group(group_id):
    documents = Document.objects.all().filter(group=group_id).order_by('order')
    return documents


# method to merge 2 documents
def merge_docs(doc1, doc2):
    # case 1: doc 1 already in group, doc 2 already in a group -> merge 2 groups
    new_group = doc1.group
    if new_group is not None:
        if doc2.group is not None:
            old_group = doc2.group
            related_documents = all_documents_in_group(old_group)
            i = 0
            for db_document in related_documents:
                db_document.group = new_group
                new_order = new_group.nrPages + i
                update_document(db_document, new_group, new_order)
                i += 1
            new_group.nrPages += i
            new_group.save()
            return new_group


@api_view(['GET'])
def document_list(request):
    if request.method == 'GET':
        documents = Document.objects.all()
        documents_serializer = DocumentSerializer(documents, many=True)
        return JsonResponse(documents_serializer.data, safe=False)


@api_view(['GET'])
def groups_list(request):
    if request.method == 'GET':
        groups = Group.objects.all()

        groups_serializer = GroupSerializer(groups, many=True)
        return JsonResponse(groups_serializer.data, safe=False)


@api_view(['GET', 'POST'])
def document(request, file_id=''):
    if request.method == 'GET':
        db_document = Document.objects.get(id=file_id)
        image_data = open(db_document.filePath, "rb").read()
        return HttpResponse(image_data, content_type="image/jpg")

    elif request.method == 'POST':
        frame = camera.get_cv_frame()

        dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_order = 0
        file_name = 'doc_' + str(file_order) + '_' + dt_string + '.jpg'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        file_group = Group(name=file_name.replace('.jpg', ''))
        file_group.save()

        cv2.imwrite(file_path, frame)

        db_document = Document(name=file_name, filePath=file_path, scanningDate=datetime.now(), group=file_group,
                               order=file_order)
        db_document.save()

        serializer = DocumentSerializer(db_document)
        return HttpResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # TODO
        Document.objects.get(name=file_id).delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def group(request, group_id=''):
    if request.method == 'GET':
        group = Group.objects.get(id=group_id)
        documents = all_documents_in_group(group_id=group)
        documents_serializer = DocumentSerializer(documents, many=True)
        return JsonResponse(documents_serializer.data, safe=False)

    elif request.method == 'POST':
        doc1_id = request.data['doc1_id']
        doc2_id = request.data['doc2_id']

        db_document1 = Document.objects.get(id=doc1_id)

        if db_document1 is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        db_document2 = Document.objects.get(id=doc2_id)

        if db_document2 is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        merge_docs(db_document1, db_document2)

        return HttpResponse(status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # TODO
        Group.objects.get(id=group_id).delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def rename_document(request):
    if request.method == 'POST':
        group_id = request.data['id']
        file_name = request.data['new_name']

        db_group = Group.objects.get(id=group_id)

        if db_group is None:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        db_group.name = file_name.replace('.jpg', '')
        db_group.save()

        related_documents = all_documents_in_group(db_group)
        for doc in related_documents:
            new_file_name = file_name.replace('.jpg', '') + str(doc.order) + '.jpg'
            doc.name = new_file_name
            old_file_path = doc.filePath
            file_path = os.path.join(settings.MEDIA_ROOT, new_file_name)
            os.rename(old_file_path, file_path)
            doc.filePath = file_path
            doc.save()

        return HttpResponse(status=status.HTTP_200_OK)


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
