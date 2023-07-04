from rest_framework import serializers

from .models import CsvFile


class CsvUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFile
        fields = ["file"]
