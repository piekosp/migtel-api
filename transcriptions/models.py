from enum import IntEnum

from django.db import models


class RecordingTranscriptionStatus(IntEnum):
    IN_PROGRESS = 1
    COMPLETED = 2
    FAILED = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name.replace("_", " ").title()) for key in cls]


class RecordingTranscriptions(models.Model):
    name = models.CharField(max_length=255)
    recording = models.FileField(upload_to="transcriptions/")
    transcription = models.TextField()
    note = models.TextField()
    status = models.IntegerField(
        choices=RecordingTranscriptionStatus.choices(),
        default=RecordingTranscriptionStatus.IN_PROGRESS.value,
    )
    created_at = models.DateTimeField(auto_now_add=True)
