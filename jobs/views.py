from rest_framework import views
from rest_framework.response import Response
from rest_framework_api_key.permissions import HasAPIKey

from .serializers import JobOfferSerializer


class JobOfferCreateView(views.APIView):
    permission_classes = [HasAPIKey]

    def post(self, request, format=None):
        serializer = JobOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
