from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from companies.serializers import CsvUploadSerializer
from users.permissions import IsManager

from .serializers import CompanyCreateSerializer, JobOfferSerializer
from .tasks import load_job_offers_from_csv, send_data


class JobOfferCreateView(views.APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, format=None):
        # Two serializers are used to separate logic of models creation
        offer_serializer = JobOfferSerializer(data=request.data)
        company_serializer = CompanyCreateSerializer(data=request.data)

        offer_serializer.is_valid(raise_exception=True)
        offer = offer_serializer.save()

        company_serializer.is_valid(raise_exception=True)
        company = company_serializer.save()

        offer.company = company
        offer.save()

        send_data.delay(company.id)

        return Response(offer_serializer.data | company_serializer.data)


class UploadOffersView(views.APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, format=None):
        serializer = CsvUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.save()

        load_job_offers_from_csv.delay(str(file))

        return Response(serializer.data)
