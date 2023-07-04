from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

api_urls = [
    path("users/", include("users.urls", namespace="users")),
    path("companies/", include("companies.urls", namespace="companies")),
    path("jobs/", include("jobs.urls", namespace="jobs")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
