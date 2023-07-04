from django.urls import path

from .views import CsvUploadView

app_name = "companies"

urlpatterns = [
    path("upload/", CsvUploadView.as_view(), name="csv_upload"),
]
