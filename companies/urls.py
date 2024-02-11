from django.urls import path

from .views import (
    CompaniesExportView,
    CompaniesListView,
    CompaniesRetrieveUpdateView,
    CsvUploadView,
    ProjectView,
    TestView,
)

app_name = "companies"

urlpatterns = [
    path("", CompaniesListView.as_view(), name="list"),
    path("<int:pk>/", CompaniesRetrieveUpdateView.as_view(), name="retrieve-update"),
    path("upload/", CsvUploadView.as_view(), name="csv_upload"),
    path("export/", CompaniesExportView.as_view(), name="csv_export"),
    path("projects/", ProjectView.as_view(), name="projects"),
    path("test/", TestView.as_view(), name="test"),
]
