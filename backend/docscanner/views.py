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


# method to get the number of documents in a group
def nb_of_documents(group_id):
    return len(all_documents_in_group(group_id))


# method to update the document on merging
def update_document(db_document, group_id, order):
    db_document.group = group_id
    db_document.order = order
    db_document.save()


# method to get a list of documents in a group
def all_documents_in_group(group_id):
    documents = Document.objects.all().filter(group=group_id)

    # documents_serializer = DocumentSerializer(documents, many=True)
    # return JsonResponse(documents_serializer.data, safe=False)
    return documents


# method to merge 2 documents
def merge_docs(doc1, doc2):
    # case 1: doc 1 already in group, doc 2 already in a group -> merge 2 groups
    if doc1.group is not None:
        if doc2.group is not None:
            oldGroup = doc2.group
            newOrder = nb_of_documents(doc1.group) + 1
            update_document(doc2, doc1.group, newOrder)
            relatedDocuments = all_documents_in_group(oldGroup)
            i = 2
            for document in relatedDocuments:
                document.group = doc1.group
                newOrder = nb_of_documents(doc1.group) + i
                update_document(document, doc1.group, newOrder)
                i += 1
                return doc1.group
        # case 2: doc 1 already in group, doc 2 in no group -> add new doc to existing group
        elif doc2.group is None:
            newOrder = nb_of_documents(doc1.group) + 1
            update_document(doc2, doc1.group, newOrder)
            return doc1.group
    # case 3: the documents are not in a group -> create new group and add docs to group
    elif doc1.group is None:
        if doc2.group is None:
            group = Group(name=doc1.name)
            group.save()

            order = 0
            update_document(doc1, group, order)
            update_document(doc2, group, order + 1)
            return doc1.group
        # case 4: doc 2 in no group, doc 2 already in a group -> add new doc to existing group
        elif doc2.group != -1:
            newOrder = nb_of_documents(doc2.group) + 1
            update_document(doc1, doc2.group, newOrder)
            return doc1.group


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
def document(request, file=''):
    if request.method == 'GET':
        image_data = open(file, "rb").read()
        return HttpResponse(image_data, content_type="image/jpg")

    elif request.method == 'POST':
        frame = camera.get_cv_frame()

        dt_string = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = 'doc_' + dt_string + '.jpg'
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        file_date = dt_string
        file_group = -1
        file_order = -1

        cv2.imwrite(file_path, frame)

        db_document = Document(name=file_name, filePath=file_path, scanningDate=file_date, group=file_group,
                               order=file_order)
        db_document.save()

        serializer = DocumentSerializer(db_document)
        return HttpResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        # TODO
        Document.objects.get(name=file).delete()
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
        Group.objects.get(name=name).delete()
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
        ret, jpeg = cv2.imencode('.jpg', frame)
        encoded_frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + encoded_frame + b'\r\n\r\n')


def camera_feed(request):
    return StreamingHttpResponse(gen(),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
