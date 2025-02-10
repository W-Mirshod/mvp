from apps.backend_mailer.serializers.files import UploadedFileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class FileUploadView(APIView):
    @swagger_auto_schema(
        operation_description="Upload a file",
        request_body=UploadedFileSerializer,
        responses={
            201: openapi.Response('Created', UploadedFileSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = UploadedFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    