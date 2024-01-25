from django.urls import path

from .views import (
    CompaniesExportView,
    CompaniesListView,
    CompaniesRetrieveUpdateView,
    CsvUploadView,
)

app_name = "companies"

urlpatterns = [
    path("", CompaniesListView.as_view(), name="list"),
    path("<int:pk>/", CompaniesRetrieveUpdateView.as_view(), name="retrieve-update"),
    path("upload/", CsvUploadView.as_view(), name="csv_upload"),
    path("export/", CompaniesExportView.as_view(), name="csv_export"),
]
