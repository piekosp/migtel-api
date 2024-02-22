from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.permissions import IsAnalyst, IsManager

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
    permission_classes = [IsAuthenticated, IsManager]
    serializer_class = ProjectSerializer


class CompaniesCollectView(views.APIView):
    permission_classes = [IsAuthenticated, IsManager, IsAnalyst]

    def get(self, request, format=None):
        user = request.user

        previous_company = Company.objects.filter(
            status__assigned_user=user,
            status__completed=False,
        ).first()

        if previous_company:
            serializer = CompanySerializer(instance=previous_company)
            return Response(status=200, data=serializer.data)

        lookup = get_lookup_for_criteria(user.project.criteria)
        next_company = (
            Company.objects.filter(
                ~Q(status__completed=True),
                Q(status__assigned_user__isnull=True),
                **lookup
            )
            .select_related("pca")
            .first()
        )
        if next_company:
            CompanyStatus.objects.create(company=next_company, assigned_user=user)
            serializer = CompanySerializer(instance=next_company)
            return Response(status=200, data=serializer.data)

        return Response(status=404)

    def post(self, request, format=None):
        company_id = request.data.get("id")
        if not company_id:
            raise Exception  # TODO: create custom exception or return 404

        instance = get_object_or_404(Company, id=company_id)
        edited_company = Company.objects.get(status__assigned_user=request.user)
        if instance != edited_company:
            raise Exception  # TODO: create custom exception or return 404

        serializer = CompanySerializer(edited_company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        company = serializer.save()

        self.complete_company_status(company)

        return Response(status=200, data=request.data)

    def complete_company_status(self, company):
        company.status.completed = True
        company.status.completed_on = datetime.now()
        company.status.save()
