from django.contrib import admin

from .models import Company, Phone, PolishClassificationOfActivities

admin.site.register(Company)
admin.site.register(PolishClassificationOfActivities)
admin.site.register(Phone)
