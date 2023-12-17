from rest_framework import serializers

from .models import Company, CsvFile, PolishClassificationOfActivities


class CsvUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFile
        fields = ["file"]


class PolishClassificationOfActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolishClassificationOfActivities
        fields = ["section", "department", "group", "industry"]


class CompanySerializer(serializers.ModelSerializer):
    pca = PolishClassificationOfActivitiesSerializer()

    class Meta:
        model = Company
        fields = [
            "nip",
            "krs",
            "regon",
            "name",
            "address1",
            "address2",
            "zip",
            "city",
            "state",
            "website",
            "facebook",
            "linkedin",
            "pca",
            "employment_range",
            "basic_legal_form",
            "specific_legal_form",
            "ownership_form",
            "establishment_date",
            "start_date",
        ]
