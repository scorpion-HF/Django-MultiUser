from django.urls import path
from . import views

app_name = "file"
urlpatterns = [
    path("file/", views.FileCustomerView.as_view(), name="file"),
    path("file-fastq/", views.FileCustomerFastqView.as_view(),
         name="file-fastq"),

    # download
    path('download/file/<str:slug>/',
         views.FileCustomerDownloadView.as_view(), name="file-download"),
    path('download/filefastq/<str:slug>/',
         views.FileCustomerFastqDownloadView.as_view(), name="file-fastq-download"),
    path('igv/<str:slug>/',
         views.FileIGVView.as_view(), name='file_igv_download'),

    # upload
    path('upload/file/<filename>/',
         views.FileCustomerUploadView.as_view(), name="file-upload"),

    path('upload/filefastq/',
         views.FileCustomerFastqUploadView.as_view(), name="file-fastq-upload"),
    # create upload
    path('upload/file/create/',
         views.FileCustomerUploadCreateView.as_view(), name="create-file-upload"),
    path('upload/filefastq/create/',
         views.FileCustomerFastqUploadCreateView.as_view(), name="create-filefastq-upload"),
]