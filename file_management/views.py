from django.shortcuts import render

from file_management.filters import FileCustomerFastqFilter, FileCustomerFilter
from .models import FileCustomer, FileCustomerFastq, FolderCustomer
from .serializers import FileCustomerFastqSerializer, FileCustomerSerializer, FolderCustomerSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FileUploadParser
from django.db.models import Q
from rest_framework import status
from django.http import StreamingHttpResponse
import os
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from wsgiref.util import FileWrapper

# from common.permissions import CheckCenterPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.views import View


# def file_iterator(file_path, chunk_size=625360):
#     with open(file_path, 'rb') as file:
#         while True:
#             data = file.read(chunk_size)
#             if not data:
#                 break
#             yield data
#
#
# def file_iterator2(file_path, start=None, end=None, chunk_size=8192):
#     with open(file_path, 'rb') as file:
#         if start is not None:
#             file.seek(start)
#         while True:
#             data = file.read(chunk_size)
#             if not data or (end is not None and file.tell() > end):
#                 break
#             yield data


def get_file_object_or_false(filename: str) -> [bool, FileCustomer, FileCustomerFastq]:
    file = FileCustomer.objects.get(public_path=filename)
    if file:
        return file
    file = FileCustomerFastq.objects.get(public_path_r1=filename)
    if file:
        return file
    file = FileCustomerFastq.objects.get(public_path_r2=filename)
    if file:
        return file
    return False


class FileCustomerUploadCreateView(APIView):
    serializer_class = FileCustomerSerializer
    # permission_classes = [IsAuthenticated, CheckCenterPermission]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.initial_data["center"] = request.user.center.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileCustomerFastqUploadCreateView(APIView):
    serializer_class = FileCustomerFastqSerializer
    # permission_classes = [IsAuthenticated, CheckCenterPermission]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.initial_data["center"] = request.user.center.id
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileCustomerView(ListAPIView):
    # permission_classes = [IsAuthenticated, CheckCenterPermission]
    permission_classes = [IsAuthenticated]
    serializer_class = FileCustomerSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FileCustomerFilter
    ordering_fields = '__all__'
    ordering = ['-id']

    def get_queryset(self):
        queryset = FileCustomer.objects.filter(center=self.request.user.center)
        queryset = self.filter_queryset(queryset)
        return queryset


class FileCustomerFastqView(ListAPIView):
    # permission_classes = [IsAuthenticated, CheckCenterPermission]
    permission_classes = [IsAuthenticated]
    serializer_class = FileCustomerFastqSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FileCustomerFastqFilter
    ordering_fields = '__all__'
    ordering = ['-id']
    search_fields = ['doc_name_r1', 'doc_name_r2']

    def get_queryset(self):
        queryset = FileCustomerFastq.objects.filter(
            center=self.request.user.center)
        queryset = self.filter_queryset(queryset)
        return queryset


class FileIGVView(APIView):
    def get(self, request, slug, r):
        igv_file = get_object_or_404(
            FileCustomerFastq, (Q(public_path_r1=slug) | Q(public_path_r2=slug)))

        byte_range = request.META.get('HTTP_RANGE')
        if igv_file.public_path_r1 == slug:
            target_file = igv_file.real_path_r1
            file_name = igv_file.doc_name_r1
        else:
            target_file = igv_file.real_path_r2
            file_name = igv_file.doc_name_r2

        if os.path.exists(target_file):
            file_size = os.path.getsize(target_file)

            if byte_range:
                start, end = byte_range.strip('bytes=').split('-')
                start = int(start)
                end = int(end) if end else file_size - 1
                start_index = start//5
                end_index = (end//5) + 1

                if start >= file_size or end >= file_size:
                    return Response(status=416)

                content_range = f'bytes {start}-{end}/{file_size}'

                response = StreamingHttpResponse(
                    FileWrapper(filelike=open(target_file, 'rb'))[start_index:end_index+1],
                    content_type='application/octet-stream',
                    status=206
                )
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                response['Content-Length'] = end - start + 1
                response['Content-Range'] = content_range
            else:
                response = StreamingHttpResponse(
                    FileWrapper(filelike=open(target_file, 'rb')),
                    content_type='application/octet-stream'
                )
                response['Content-Disposition'] = f'attachment; filename="{file_name}"'
                response['Content-Length'] = file_size
            return response
        else:
            return Response(status=404)


class FileCustomerUploadView(APIView):
    parser_classes = [FileUploadParser]
    permission_classes = [AllowAny, ]

    def put(self, request, filename, format=None):
        file_object = get_file_object_or_false(filename=filename)
        if not file_object:
            return Response({"message": "The file you are looking for is not found"}, status=status.HTTP_404_NOT_FOUND)

        file = request.data['file']
        if type(file_object) == FileCustomer:
            with open(file_object.realpath, 'wb+') as f:
                for chunk in file.cunks():
                    f.write(chunk)
            return Response({"message": "File was uploaded successfully!"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"message": "File is not supposed to be of this type"}, status=status.HTTP_400_BAD_REQUEST)

class FileCustomerFastqUploadView(APIView):
    parser_classes = [FileUploadParser]
    # permission_classes = [IsAuthenticated, CheckCenterPermission]
    permission_classes = [IsAuthenticated]

    def put(self, request, filename, r, format=None):
        file_object = get_file_object_or_false(filename=filename)
        if not file_object:
            return Response({"message": "The file you are looking for is not found"},
                            status=status.HTTP_404_NOT_FOUND)

        file = request.data['file']
        if type(file_object) == FileCustomerFastq:
            if r == "r1":
                with open(file_object.real_path_r1, 'wb+') as f:
                    for chunk in file.cunks():
                        f.write(chunk)
                return Response({"message": "File was uploaded successfully!"},
                                status=status.HTTP_204_NO_CONTENT)
            elif r == "r2":
                with open(file_object.real_path_r1, 'wb+') as f:
                    for chunk in file.cunks():
                        f.write(chunk)
                return Response({"message": "File was uploaded successfully!"},
                                status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"message": "invalid argument r, set r with r1 or r2"},
                                status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "File is not supposed to be of this type"},
                        status=status.HTTP_400_BAD_REQUEST)

class FileCustomerDownloadView(APIView):
    # permission_classes = [IsAuthenticated, CheckCenterPermission]
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        file_customer = get_object_or_404(FileCustomer, public_path=slug)
        target_file = file_customer.realpath
        file_name = file_customer.doc_name

        if os.path.exists(target_file):
            response = StreamingHttpResponse(FileWrapper(filelike=open(target_file, "rb")),
                                             content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                file_name)
            response['Content-Length'] = os.path.getsize(target_file)
            return response
        else:
            return Response(status=404)

class FileCustomerFastqDownloadView(APIView):
    # permission_classes = [IsAuthenticated, CheckCenterPermission]
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        # here we should check user center also. user.center == file.center
        fastq_file = get_object_or_404(
            FileCustomerFastq, (Q(public_path_r1=slug) | Q(public_path_r2=slug)))
        if fastq_file.public_path_r1 == slug:
            target_file = fastq_file.real_path_r1
            file_name = fastq_file.doc_name_r1
        else:
            target_file = fastq_file.real_path_r2
            file_name = fastq_file.doc_name_r2

        # return Response({"target": target_file, "file":file_name})
        if os.path.exists(target_file):
            response = StreamingHttpResponse(FileWrapper(filelike=open(target_file, "rb")),
                                             content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(
                file_name)
            response['Content-Length'] = os.path.getsize(target_file)
            return response
        else:
            return Response(status=404)
