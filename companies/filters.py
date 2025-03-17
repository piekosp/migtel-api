import django_filters
from django.db.models import Q

from .models import Company


class CompanyFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="filter_by_keyword")
    pca_section = django_filters.CharFilter(
        field_name="pca__section", method="keyword_in"
    )
    pca_department = django_filters.CharFilter(
        field_name="pca__department", method="keyword_in"
    )
    pca_group = django_filters.CharFilter(field_name="pca__group", method="keyword_in")
    state = django_filters.CharFilter(field_name="state", method="keyword_in")
    employment_range = django_filters.CharFilter(
        field_name="employment_range", method="keyword_in"
    )

    def filter_by_keyword(self, queryset, _, value):
        return queryset.filter(Q(nip__icontains=value) | Q(name__icontains=value))

    def keyword_in(self, queryset, name, value):
        lookup = "__".join([name, "in"])
        values = value.split(",")
        return queryset.filter(**{lookup: values})

    class Meta:
        model = Company
        fields = [
            "search",
            "pca_section",
            "pca_department",
            "pca_group",
            "state",
            "employment_range",
        ]
