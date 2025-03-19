from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import DefaultPagination

from .models import RecordingTranscriptions
from .serializers import RecordingTranscriptionSerializer
from .tasks import transcribe


class RecordingsUploadViewSet(viewsets.ViewSet, DefaultPagination):
    permission_classes = [IsAuthenticated]
    pagination_class = DefaultPagination

    def get_queryset(self):
        return RecordingTranscriptions.objects.all().order_by("-created_at")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset, request, view=self)
        serializer = RecordingTranscriptionSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=["get"])
    def transcription(self, request, pk, *args, **kwargs):
        recording = get_object_or_404(self.get_queryset(), pk=pk)
        response = HttpResponse(recording.transcription, content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{recording.name}_transcription.txt"'
        return response

    @action(detail=True, methods=["get"])
    def note(self, request, pk, *args, **kwargs):
        recording = get_object_or_404(self.get_queryset(), pk=pk)
        response = HttpResponse(recording.note, content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = f'attachment; filename="{recording.name}_note.txt"'
        return response

    def create(self, request, *args, **kwargs):
        serializer = RecordingTranscriptionSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            transcribe.delay(instance.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
