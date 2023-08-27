from rest_framework import serializers

from companies.models import Company as MatchedCompany
from companies.models import PolishClassificationOfActivities

from .models import Company, EmploymentType, JobOffer, LegalForm


class JobOfferSerializer(serializers.Serializer):
    offer_id = serializers.UUIDField(required=False)
    offer_url = serializers.CharField(max_length=300)
    job_title = serializers.CharField(max_length=255)
    salary_range = serializers.CharField(max_length=255, required=False)
    location = serializers.CharField(max_length=255, required=False)
    employment_contract = serializers.CharField(max_length=255, required=False)
    employment_type = serializers.CharField(max_length=255, required=False)
    working_time = serializers.CharField(max_length=255, required=False)
    responsibilities = serializers.CharField(required=False)
    requirements = serializers.CharField(required=False)
    preferred = serializers.CharField(required=False)
    offered = serializers.CharField(required=False)
    benefits = serializers.CharField(required=False)
    created = serializers.DateField(required=False)
    updated = serializers.DateField(required=False)

    def create(self, validated_data):
        employment_type = validated_data.pop("employment_type", None)
        offer_url = validated_data.pop("offer_url", None)

        employment_type = employment_type.split(",")[0]
        if employment_type:
            employment_type_object, _ = EmploymentType.objects.get_or_create(
                name=employment_type
            )
        else:
            employment_type_object = None

        job_offer, _ = JobOffer.objects.get_or_create(offer_url=offer_url)
        job_offer.update(**validated_data)
        job_offer.employment_type = employment_type_object
        job_offer.save()

        return job_offer


class CompanySerializer(serializers.ModelSerializer):
    offers = JobOfferSerializer(many=True, read_only=True)
    total_offers = serializers.IntegerField()
    employment_rank = serializers.IntegerField()
    last_3m = serializers.IntegerField()
    last_6m = serializers.IntegerField()
    last_12m = serializers.IntegerField()

    legal_form = serializers.SerializerMethodField()
    legal_form_rank = serializers.SerializerMethodField()
    pca = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = [
            "company_id",
            "name",
            "nip",
            "krs",
            "regon",
            "legal_form",
            "legal_form_rank",
            "pca",
            "address",
            "zip",
            "city",
            "phone",
            "email",
            "website",
            "employment_rank",
            "employment_range",
            "total_offers",
            "last_3m",
            "last_6m",
            "last_12m",
            "offers",
        ]

    def get_legal_form(self, obj):
        return obj.legal_form.name

    def get_legal_form_rank(self, obj):
        return obj.legal_form.rank

    def get_pca(self, obj):
        return str(obj.pca)


class CompanyCreateSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    website = serializers.CharField(required=False, allow_blank=True)
    nip = serializers.CharField(required=True)
    krs = serializers.CharField(required=False)
    regon = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    zip = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    legal_form = serializers.CharField(required=False)
    pca = serializers.CharField(required=False)
    establishment_date = serializers.DateField(required=False)

    def create(self, validated_data):
        nip = validated_data.pop("nip", None)
        company_name = validated_data.get("company_name", None)
        legal_form = validated_data.pop("legal_form", None)
        pca = validated_data.pop("pca", None)

        company, _ = Company.objects.get_or_create(nip=nip)

        try:
            matched_comapny = MatchedCompany.objects.get(nip=nip) if nip else None
        except MatchedCompany.DoesNotExist:
            matched_comapny = None

        if legal_form:
            legal_form_object, _ = LegalForm.objects.get_or_create(name=legal_form)
        else:
            legal_form_object = None

        try:
            pca_object = (
                PolishClassificationOfActivities.objects.get(group=pca) if pca else None
            )
        except PolishClassificationOfActivities.DoesNotExist:
            pca_object = None

        company.update(**validated_data)
        company.matched_company = matched_comapny
        company.legal_form = legal_form_object
        company.pca = pca_object
        company.name = company_name
        company.save()

        return company
