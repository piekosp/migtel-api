import datetime
import uuid

from django.db import models

from companies.models import Company as MatchedCompany
from companies.models import PolishClassificationOfActivities


class AbstractRankModel(models.Model):
    RANK_1 = 4
    RANK_2 = 3
    RANK_3 = 2
    RANK_4 = 1
    RANK_5 = 0

    RANKS = (
        (RANK_1, 4),
        (RANK_2, 3),
        (RANK_3, 2),
        (RANK_4, 1),
        (RANK_5, 0),
    )

    name = models.CharField(max_length=50)
    rank = models.IntegerField(choices=RANKS, default=RANK_3)

    def __str__(self):
        return f"{self.name} ({self.rank})"

    class Meta:
        abstract = True


class EmploymentType(AbstractRankModel):
    """Employment type model"""


class LegalForm(AbstractRankModel):
    """Legal form model"""


class Company(models.Model):
    company_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    nip = models.CharField(null=True, blank=True, max_length=10, unique=True)
    regon = models.CharField(null=True, blank=True, max_length=20)
    krs = models.CharField(null=True, blank=True, max_length=20)
    address = models.CharField(null=True, blank=True, max_length=255)
    zip = models.CharField(null=True, blank=True, max_length=10)
    city = models.CharField(null=True, blank=True, max_length=50)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    employment_range = models.IntegerField(blank=True, null=True)
    legal_form = models.ForeignKey(LegalForm, null=True, on_delete=models.SET_NULL)
    pca = models.ForeignKey(
        PolishClassificationOfActivities,
        null=True,
        on_delete=models.SET_NULL,
        related_name="jobs_company",
    )
    establishment_date = models.DateField(null=True, blank=True)
    matched_company = models.ForeignKey(
        MatchedCompany, null=True, on_delete=models.SET_NULL
    )

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        return self.name


class JobOffer(models.Model):
    offer_id = models.UUIDField(default=uuid.uuid4, editable=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="offers", null=True
    )
    offer_url = models.CharField(max_length=300, unique=True)
    job_title = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    salary_range = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    employment_contract = models.CharField(max_length=255, blank=True, null=True)
    employment_type = models.ForeignKey(
        EmploymentType, on_delete=models.CASCADE, null=True
    )
    working_time = models.CharField(max_length=50, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    preferred = models.TextField(blank=True, null=True)
    offered = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    created = models.DateField(default=datetime.date.today, editable=False, blank=True)
    updated = models.DateField(default=datetime.date.today, blank=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __str__(self):
        if self.company:
            return f"{self.job_title} - {self.company.name}"
        return self.job_title
