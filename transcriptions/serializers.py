from rest_framework import serializers

from .models import RecordingTranscriptions


class RecordingTranscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingTranscriptions
        fields = ["id", "name", "recording", "status"]
        read_only_fields = ["id", "status"]
        extra_kwargs = {
            "recording": {"write_only": True},
        }
