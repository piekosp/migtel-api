import json

import requests
from django.conf import settings

from companies.models import PolishClassificationOfActivities

from .models import Company, EmploymentType, JobOffer, LegalForm


class JobOfferDataExtractor:
    def __init__(self, row):
        self.row = row

    def extract_data(self):
        return self.job_offer

    @property
    def pca(self):
        try:
            pca_object = (
                PolishClassificationOfActivities.objects.get(group=self.row["pca"])
                if self.row["pca"]
                else None
            )
        except PolishClassificationOfActivities.DoesNotExist:
            pca_object = None

        return pca_object

    @property
    def legal_form(self):
        if self.row["legal_form"]:
            legal_form_object, _ = LegalForm.objects.get_or_create(
                name=self.row["legal_form"]
            )
        else:
            legal_form_object = None

        return legal_form_object

    @property
    def company(self):
        company_data = {
            "krs": self.row["krs"],
            "regon": self.row["regon"],
            "name": self.row["company_name"],
            "address": self.row["street"],
            "zip": self.row["zip"],
            "city": self.row["city"],
            "phone": self.row["phone"],
            "establishment_date": self.row["establishment_date"]
            if self.row["establishment_date"]
            else None,
        }

        company_object, created = Company.objects.get_or_create(
            nip=self.row["nip"], defaults=company_data
        )
        if created:
            company_object.pca = self.pca
            company_object.legal_form = self.legal_form
            company_object.save()

        return company_object

    @property
    def employment_type(self):
        if self.row["employment_type"]:
            employment_type_object, _ = EmploymentType.objects.get_or_create(
                name=self.row["employment_type"]
            )
        else:
            employment_type_object = None

        return employment_type_object

    @property
    def job_offer(self):
        job_offer_data = {
            "job_title": self.row["job_title"],
            "salary_range": self.row["salary_range"],
            "location": self.row["location"],
            "employment_contract": self.row["employment_contract"],
            "working_time": self.row["working_time"],
            "responsibilities": self.row["responsibilities"],
            "requirements": self.row["requirements"],
            "preferred": self.row["preferred"],
            "offered": self.row["offered"],
            "benefits": self.row["benefits"],
        }

        job_offer_object, created = JobOffer.objects.get_or_create(
            offer_url=self.row["offer_url"], defaults=job_offer_data
        )

        if created:
            job_offer_object.employment_type = self.employment_type
            job_offer_object.company = self.company
            job_offer_object.save()

        return job_offer_object


class WorkbeeApi:
    AUTH = {
        "user": settings.WORKBEE_USER,
        "password": settings.WORKBEE_PASSWORD,
        "baseId": settings.WORKBEE_ID,
    }

    @classmethod
    def send_data(cls, data):
        payload = cls.AUTH | data
        requests.post(url=settings.WORKBEE_URL, json=payload)
