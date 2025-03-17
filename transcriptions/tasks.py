from celery import shared_task

from .models import RecordingTranscriptions, RecordingTranscriptionStatus
from .utils import get_transcription


@shared_task()
def transcribe(recording_transcription_id):
    recording_transcription = RecordingTranscriptions.objects.get(id=recording_transcription_id)
    try:
        transcription = get_transcription(recording_transcription)
    except Exception as e:
        recording_transcription.status = RecordingTranscriptionStatus.FAILED.value
        recording_transcription.save()
        print("Transcription failed", e)
        return
    recording_transcription.transcription = transcription["transcription"]
    recording_transcription.note = transcription["notes"]
    recording_transcription.status = RecordingTranscriptionStatus.COMPLETED.value
    recording_transcription.save()
