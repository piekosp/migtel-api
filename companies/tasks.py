from celery import shared_task

from api.utils import File, FileExporter, FileImporter, send_email

from .utils import CompanyDataExporter, CompanyDataImporter


@shared_task()
def load_companies_from_csv(file_path):
    file = File(file_path)
    importer = FileImporter(file, data_extractor=CompanyDataImporter)
    companies = importer.load_data()
    for company in companies:
        company.save()


@shared_task
def export_companies_to_csv(data):
    data_exporter = CompanyDataExporter(data)
    file_exporter = FileExporter(data_exporter, "companies")
    file = file_exporter.export_file()
    send_email(
        "Download your file",
        file.get_url(),
        "pawel@piekos.pl",
    )
