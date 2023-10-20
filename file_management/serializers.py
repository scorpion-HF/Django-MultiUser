from rest_framework import serializers
from .models import FileCustomer, FileCustomerFastq, FolderCustomer


class FileCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileCustomer
        exclude = ['realpath', 'run']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('center', None)
        return representation


class FileCustomerFastqSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileCustomerFastq
        exclude = ['real_path_r1', 'real_path_r2', 'run']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('center', None)
        return representation


class FolderCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderCustomer
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('center', None)

        return representation
