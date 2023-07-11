from django.urls import path

from .views import JobOfferCreateView

app_name = "jobs"

urlpatterns = [
    path("", JobOfferCreateView.as_view(), name="job_offer_create"),
]
