import logging
from rest_framework.exceptions import APIException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from apps.email_analysis.serializers.email_analysis_serializers import SpamDetectionInputSerializer, EmailPersonalizationInputSerializer
from apps.email_analysis.services.ai_functions import classify_email,personalize_email


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

            if "email_content" not in request.data:
                return Response(
                    {"error": "Email content is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer.is_valid(raise_exception=True)
            email_content = serializer.validated_data["email_content"]

            is_spam = classify_email(email_content)

            return Response(
                {
                    "is_spam": is_spam,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class EmailPersonalizationView(APIView):
    @swagger_auto_schema(
        operation_summary="Generate a personalized version of an email",
        operation_description="Takes an email content and rewrites it in a more engaging and friendly way.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email_content": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The content of the email to personalize",
                    example="Hello, we have a special offer just for you!",
                ),
                "personalization_hint": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="Hint to guide the personalization (optional)",
                    example="Make it more friendly",
                    default="Make it more friendly",
                ),
            },
            required=["email_content"],
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "personalized_email": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description="Rewritten, more engaging email content",
                        example="Hey there! We've got an exclusive deal just for you! 🎉 Check it out now!",
                    ),
                },
            ),
            400: openapi.Response(
                description="Bad Request",
                examples={"application/json": {"error": "Email content is required"}},
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        """
        API endpoint to personalize an email using Ollama.
        """
        try:
            serializer = EmailPersonalizationInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email_content = serializer.validated_data["email_content"]
            user = request.user

            personalized_email = personalize_email(user, email_content)

            if not personalized_email:
                return Response(
                    {"error": "Failed to generate personalized email"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            return Response(
                {
                    "personalized_email": personalized_email,
                },
                status=status.HTTP_200_OK,
            )

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)
