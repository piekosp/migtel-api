from django.contrib import admin

from .models import Company, CompanyStatus, PolishClassificationOfActivities, Project

admin.site.register(Company)
admin.site.register(PolishClassificationOfActivities)
admin.site.register(Project)
admin.site.register(CompanyStatus)
