from rest_framework import serializers

from companies.models import Company as MatchedCompany

from .models import Company, JobOffer


class JobOfferSerializer(serializers.Serializer):
    company_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(
        max_length=14, required=False, allow_blank=True
    )
    offer_url = serializers.CharField(max_length=300)
    job_title = serializers.CharField(max_length=255)
    company_description = serializers.CharField(required=False)
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
    nip = serializers.CharField(required=False)

    def create(self, validated_data):
        data = validated_data.copy()
        company_name = validated_data.pop("company_name")
        phone_number = validated_data.pop("phone_number", None)
        nip = validated_data.pop("nip", None)

        company, _ = Company.objects.get_or_create(name=company_name)

        try:
            matched_comapny = MatchedCompany.objects.get(nip=nip) if nip else None
        except MatchedCompany.DoesNotExist:
            matched_comapny = None

        company.phone_number = phone_number or company.phone_number
        company.nip = nip or company.nip
        company.matched_company = matched_comapny or company.matched_company
        company.save()

        job_offer = JobOffer.objects.filter(offer_url=validated_data["offer_url"])

        if not job_offer.exists():
            JobOffer.objects.create(company=company, **validated_data)
        else:
            job_offer.update(**validated_data)

        return data
