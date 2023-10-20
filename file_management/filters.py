import django_filters
from file_management.models import FileCustomer, FileCustomerFastq


class FileCustomerFilter(django_filters.FilterSet):
    class Meta:
        model = FileCustomer
        fields = {
            'doc_name': ['icontains'],
            'doc_type': ['exact'],
            'center__name': ['exact'],
            'important': ['exact'],
            'deleted': ['exact'],
        }


class FileCustomerFastqFilter(django_filters.FilterSet):
    class Meta:
        model = FileCustomerFastq
        fields = {
            'doc_name_r1': ['icontains'],
            'doc_name_r2': ['icontains'],
            'center__name': ['exact'],
            'important': ['exact'],
            'deleted': ['exact'],
        }
