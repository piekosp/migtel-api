import csv
import io
import logging
import os

import pandas as pd
import shortuuid
from django.conf import settings
from django.core.files.base import ContentFile
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Mail

from .storages import MediaStorage

logger = logging.getLogger(__name__)


def send_email(subject, content, recipient):
    message = Mail(
        from_email=settings.SENGRID_FROM_EMAIL,
        to_emails=recipient,
        subject=subject,
        html_content=Content("text/plain", content),
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        sg.send(message)
    except Exception as e:
        logger.error("Error sending email: ", e)


class File:
    def __init__(self, location):
        self.location = location

    def get_url(self):
        file_url = settings.MEDIA_URL + self.location
        if not settings.USE_S3:
            file_url = settings.BASE_URL + file_url
        return file_url

    def get_root(self):
        return settings.MEDIA_ROOT + self.location


class FileImporter:
    def __init__(self, file: File, data_extractor):
        self.file = file
        self.data_extractor = data_extractor

    def load_data(self):
        reader = pd.read_csv(
            self.file.get_root(), delimiter=";", dtype=str, keep_default_na=False
        )
        for _, row in reader.iterrows():
            extractor = self.data_extractor(row)
            data = extractor.extract_data()
            yield data


class FileExporter:
    def __init__(self, data_exporter, location):
        self.storage = MediaStorage()
        self.data_exporter = data_exporter
        self.file_name = self.get_file_name()
        self.location = location
        self.exported = False

    def get_file_name(self):
        return shortuuid.uuid() + ".csv"

    def get_absolute_path(self):
        directory_path = os.path.join(settings.MEDIA_ROOT, self.location)
        return os.path.join(directory_path, self.file_name)

    def get_relative_path(self):
        return os.path.join(self.location, self.file_name)

    def _export_locally(self):
        file_path = self.get_absolute_path()
        with open(file_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=self.data_exporter.get_headers())
            writer.writeheader()
            for row in self.data_exporter.get_row():
                writer.writerow(row)

    def _export_to_s3(self):
        with io.StringIO() as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=self.data_exporter.get_headers()
            )
            writer.writeheader()
            for row in self.data_exporter.get_row():
                writer.writerow(row)
            csvfile.seek(0)
            content = csvfile.getvalue().encode("utf-8")

        self.storage.save(self.get_relative_path(), ContentFile(content))

    def export_file(self):
        if self.exported:
            raise Exception("File already created")
        if settings.USE_S3:
            self._export_to_s3()
        else:
            self._export_locally()

        self.exported = True
        return File(self.get_relative_path())
