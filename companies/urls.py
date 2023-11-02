from django.urls import path

from .views import CompaniesListView, CsvUploadView

app_name = "companies"

urlpatterns = [
    path("", CompaniesListView.as_view(), name="companies"),
    path("upload/", CsvUploadView.as_view(), name="csv_upload"),
]
