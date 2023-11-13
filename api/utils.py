import csv
import logging
import os

import pandas as pd
import shortuuid
from django.conf import settings
from django.utils.text import slugify
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Content, Mail

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


class FileImporter:
    def __init__(self, file_path, data_extractor):
        self.file_location = settings.MEDIA_LOCATION + file_path
        self.data_extractor = data_extractor

    def load_data(self):
        reader = pd.read_csv(
            self.file_location, delimiter=";", dtype=str, keep_default_na=False
        )
        for _, row in reader.iterrows():
            extractor = self.data_extractor(row)
            data = extractor.extract_data()
            yield data


class File:
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def get_url(self):
        return settings.MEDIA_LOCATION + self.location


class FileExporter:
    def __init__(self, data_exporter, location):
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

    def export_file(self):
        if self.exported:
            raise Exception("File already created")
        file_path = self.get_absolute_path()
        with open(file_path, "w") as file:
            writer = csv.DictWriter(file, fieldnames=self.data_exporter.get_headers())
            writer.writeheader()
            for row in self.data_exporter.get_row():
                writer.writerow(row)

        self.exported = True
        return File(self.file_name, self.get_relative_path())
