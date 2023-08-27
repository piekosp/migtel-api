from celery import shared_task

from api.utils import FileImporter

from .utils import CompanyDataExtractor


@shared_task()
def load_companies_from_csv(file_path):
    importer = FileImporter(file_path, data_extractor=CompanyDataExtractor)
    importer.load_data()
