from rest_framework import views
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsManager

from .filters import CompanyFilter
from .models import Company
from .serializers import CompanySerializer, CsvUploadSerializer
from .tasks import load_companies_from_csv


class CsvUploadView(views.APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request, format=None):
        serializer = CsvUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.save()

        load_companies_from_csv.delay(str(file))

        return Response(serializer.data)


class CompaniesListView(ListAPIView):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = CompanySerializer
    filterset_class = CompanyFilter
