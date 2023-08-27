from django.urls import path

from .views import JobOfferCreateView, UploadOffersView

app_name = "jobs"

urlpatterns = [
    path("", JobOfferCreateView.as_view(), name="job_offer_create"),
    path("upload/", UploadOffersView.as_view(), name="job_offer_upload"),
]
