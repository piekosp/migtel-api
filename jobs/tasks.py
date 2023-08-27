import datetime
import json

from celery import shared_task
from django.db.models import Avg, Case, Count, Q, When

from api.utils import FileImporter

from .models import Company
from .serializers import CompanySerializer
from .utils import JobOfferDataExtractor, WorkbeeApi


@shared_task()
def send_data(company_id):
    last_3m = (
        datetime.date.today() - datetime.timedelta(days=(365 * 3 / 12))
    ).isoformat()
    last_6m = (
        datetime.date.today() - datetime.timedelta(days=(365 * 6 / 12))
    ).isoformat()
    last_12m = (datetime.date.today() - datetime.timedelta(days=365)).isoformat()
    queryset = (
        Company.objects.prefetch_related("offers")
        .prefetch_related("offers__employment_type")
        .select_related("legal_form")
        .select_related("pca")
        .annotate(employment_rank=Avg("offers__employment_type__rank"))
        .annotate(total_offers=Count("offers"))
        .annotate(last_3m=Count(Case(When(Q(offers__created__gte=last_3m), then=1))))
        .annotate(last_6m=Count(Case(When(Q(offers__created__gte=last_6m), then=1))))
        .annotate(last_12m=Count(Case(When(Q(offers__created__gte=last_12m), then=1))))
        .get(id=company_id)
    )
    company = CompanySerializer(queryset)
    WorkbeeApi.send_data(company.data)


@shared_task()
def load_job_offers_from_csv(file_path):
    importer = FileImporter(file_path, data_extractor=JobOfferDataExtractor)
    offers = importer.load_data()
    for offer in offers:
        send_data(offer.company.id)
