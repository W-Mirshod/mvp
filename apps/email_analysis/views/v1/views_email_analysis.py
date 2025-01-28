import logging
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.email_analysis.serializers.email_analysis_serializers import SpamDetectionInputSerializer
from apps.email_analysis.services.spam_detection_service import classify_email


logger = logging.getLogger(__name__)

class SpamDetectionView(APIView):
    @swagger_auto_schema(
        operation_summary="Detect if an email is spam",
        operation_description="Takes the email content as input and determines whether it is spam.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email_content": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The content of the email to analyze",
                    example="This is a test email to check for spam.",
                ),
            },
            required=["email_content"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "is_spam": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        description="Result of the spam detection",
                        example=False,
                    ),
                },
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={
                    "application/json": {
                        "error": "Email content is required"
                    }
                },
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = SpamDetectionInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email_content = serializer.validated_data["email_content"]

            is_spam = classify_email(email_content)

            return Response(
                {
                    "is_spam": is_spam,
                },
                status=status.HTTP_200_OK,
            )

        except APIException as e:
            logger.warning(f"Validation error: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)
