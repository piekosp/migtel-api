import numpy as np
import pandas as pd
from celery import shared_task
from django.conf import settings
from django.db import IntegrityError

from .models import Company, Email, Phone, PolishClassificationOfActivities
from .utils import extract_data_from_file


@shared_task()
def load_companies_from_csv(file_name):
    # settings.MEDIA_ROOT + "/" + file_name
    file_path = settings.BASE_URL + settings.MEDIA_URL + file_name
    reader = pd.read_csv(file_path, delimiter=";", dtype=str)
    reader = reader.replace(np.nan, None)
    for _, row in reader.iterrows():
        data = extract_data_from_file(row)
        pca, _ = PolishClassificationOfActivities.objects.get_or_create(**data["pca"])
        try:
            company, _ = Company.objects.get_or_create(pca=pca, **data["company"])
        except IntegrityError:
            continue

        for phone in data["phones"]:
            Phone.objects.get_or_create(number=phone, company=company)
        for email in data["emails"]:
            Email.objects.get_or_create(address=email, company=company)
