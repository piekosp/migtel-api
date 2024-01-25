from rest_framework import serializers

from .models import Company, CsvFile, PolishClassificationOfActivities


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


class CompanyUpdateSerializer(serializers.ModelSerializer):
    pca = PCAField()

    class Meta:
        model = Company
        fields = [
            "id",
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
        ]


class CompanySerializer(serializers.ModelSerializer):
    pca = PCAField()
    phones = serializers.SerializerMethodField()
    emails = serializers.SerializerMethodField()

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
            "phones",
            "emails",
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

    def get_phones(self, obj):
        return list(obj.phone_set.values_list("number", flat=True))

    def get_emails(self, obj):
        return list(obj.email_set.values_list("address", flat=True))
