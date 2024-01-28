from rest_framework import status, views
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsManager

from .filters import CompanyFilter
from .models import Company
from .serializers import CompanySerializer, CsvUploadSerializer
from .tasks import export_companies_to_csv, load_companies_from_csv


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


class CompaniesRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = CompanySerializer


class CompaniesExportView(views.APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, format=None):
        filter = CompanyFilter(request.GET, queryset=Company.objects.all())
        if filter.is_valid():
            items_count = filter.qs.count()
            serializer = CompanySerializer(filter.qs, many=True)
            export_companies_to_csv.delay()(serializer.data)
            return Response({"items_count": items_count})
        return Response(status=status.HTTP_204_NO_CONTENT)
