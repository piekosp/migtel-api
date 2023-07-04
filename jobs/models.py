from django.db import models

from companies.models import Company as MatchedCompany


class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    nip = models.CharField(null=True, blank=True, unique=True, max_length=10)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    employment_range = models.IntegerField(blank=True, null=True)
    matched_company = models.ForeignKey(
        MatchedCompany, null=True, on_delete=models.SET_NULL
    )


class JobOffer(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    offer_url = models.CharField(max_length=300, unique=True)
    job_title = models.CharField(max_length=255)
    company_description = models.TextField(blank=True, null=True)
    salary_range = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    employment_contract = models.CharField(max_length=255, blank=True, null=True)
    employment_type = models.CharField(max_length=255, blank=True, null=True)
    working_time = models.CharField(max_length=50, blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    preferred = models.TextField(blank=True, null=True)
    offered = models.TextField(blank=True, null=True)
    benefits = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
