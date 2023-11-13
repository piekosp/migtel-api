from django.urls import path

from .views import CompaniesExportView, CompaniesListView, CsvUploadView

app_name = "companies"

urlpatterns = [
    path("", CompaniesListView.as_view(), name="list"),
    path("upload/", CsvUploadView.as_view(), name="csv_upload"),
    path("export/", CompaniesExportView.as_view(), name="csv_export"),
]
