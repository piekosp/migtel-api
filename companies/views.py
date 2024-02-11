from django.db.models import Q
from rest_framework import status, views
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsManager

from .filters import CompanyFilter
from .models import Company, CompanyStatus, Project
from .serializers import CompanySerializer, CsvUploadSerializer, ProjectSerializer
from .tasks import export_companies_to_csv, load_companies_from_csv
from .utils import get_lookup_for_criteria


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


class ProjectView(ListCreateAPIView):
    queryset = Project.objects.all()
    # permission_classes = [IsAuthenticated, IsManager]
    serializer_class = ProjectSerializer


class TestView(views.APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request, format=None):
        user = request.user
        assigned_company = Company.objects.filter(
            status__assigned_user=user,
            status__completed=False,
        ).first()

        if assigned_company:
            serializer = CompanySerializer(instance=assigned_company)
            return Response(status=200, data=serializer.data)

        project = Project.objects.get(id=2)
        lookup = get_lookup_for_criteria(project.criteria)
        company = (
            Company.objects.filter(
                ~Q(status__completed=True), ~Q(status__taken=True), **lookup
            )
            .select_related("pca")
            .first()
        )
        if company:
            CompanyStatus.objects.create(
                company=company, assigned_user=user, taken=True
            )
            serializer = CompanySerializer(instance=company)
            return Response(status=200, data=serializer.data)

        return Response(status=404)
