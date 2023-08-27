import pandas as pd
from django.conf import settings


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
