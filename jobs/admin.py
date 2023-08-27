from django.contrib import admin

from .models import Company, EmploymentType, JobOffer, LegalForm

admin.site.register([Company, JobOffer, EmploymentType, LegalForm])
