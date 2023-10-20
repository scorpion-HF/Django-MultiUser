from django.db import models
import uuid


# TODO: what is center and run
class FileCustomer(models.Model):
    DOC_TYPE_CHOICES = [
        ('VCF', 'vcf'),
        ('CRAM', 'cram'),
        ('CRAI', 'crai'),
        ('BAM', 'bam'),
        ('BAI', 'bai'),
        ('Annotation', 'annotation'),
    ]
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    doc_name = models.CharField(max_length=250)
    doc_type = models.CharField(
        max_length=10, choices=DOC_TYPE_CHOICES, default="VCF")
    # center = models.ForeignKey("ilcore.Center", on_delete=models.CASCADE)
    public_path = models.UUIDField(unique=True, default=uuid.uuid4)
    realpath = models.CharField(
        max_length=250, default=None, null=True, blank=True)
    size = models.IntegerField(default=0)
    important = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    # run = models.ManyToManyField(
    #     "run.Run", related_name="files", blank=True)

    class Meta:
        verbose_name_plural = "Files"
        verbose_name = "File"
        indexes = [
            models.Index(fields=['doc_name', 'doc_type', 'center']),
        ]


# TODO: what is center and run
class FileCustomerFastq(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # center = models.ForeignKey("ilcore.Center", on_delete=models.CASCADE)
    doc_name_r1 = models.CharField(max_length=2500)
    doc_name_r2 = models.CharField(max_length=2500)
    public_path_r1 = models.UUIDField(unique=True, default=uuid.uuid4)
    public_path_r2 = models.UUIDField(unique=True, default=uuid.uuid4)
    real_path_r1 = models.CharField(
        max_length=2500, default=None, null=True, blank=True)
    real_path_r2 = models.CharField(
        max_length=2500, default=None, null=True, blank=True)
    size_r1 = models.BigIntegerField(default=0)
    size_r2 = models.BigIntegerField(default=0)
    important = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    # run = models.ManyToManyField(
    #     "run.Run", related_name="files_fastq", blank=True)

    class Meta:
        verbose_name_plural = "FileFastqs"
        verbose_name = "FileFastq"
        indexes = [
            models.Index(fields=['doc_name_r1', 'doc_name_r2', 'center']),
        ]


# TODO: what is center and run
class FolderCustomer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # center = models.ForeignKey("ilcore.Center", on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=250)
    real_path = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Folders"
        verbose_name = "Folder"
