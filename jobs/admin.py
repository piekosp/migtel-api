from django.contrib import admin

from .models import Company, JobOffer

admin.site.register([Company, JobOffer])
