from rest_framework import serializers

from .models import Company, CsvFile, PolishClassificationOfActivities, Project


class PCAField(serializers.Field):
    def to_representation(self, value):
        return PolishClassificationOfActivitiesSerializer(value).data

    def to_internal_value(self, data):
        try:
            return PolishClassificationOfActivities.objects.get(group=data["group"])
        except (AttributeError, KeyError):
            pass


class CsvUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CsvFile
        fields = ["file"]


class PolishClassificationOfActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolishClassificationOfActivities
        fields = ["section", "department", "group", "industry"]


class CompanySerializer(serializers.ModelSerializer):
    pca = PCAField()

    class Meta:
        model = Company
        fields = [
            "id",
            "nip",
            "krs",
            "regon",
            "name",
            "address1",
            "address2",
            "zip",
            "city",
            "state",
            "phone1",
            "phone2",
            "email1",
            "email2",
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
        read_only_fields = [
            "nip",
            "krs",
            "regon",
            "establishment_date",
            "start_date",
        ]


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["name", "criteria"]
