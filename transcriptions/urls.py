from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RecordingsUploadViewSet

app_name = "transcriptions"

router = DefaultRouter()
router.register(r"", RecordingsUploadViewSet, basename="transcriptions")
urlpatterns = router.urls
