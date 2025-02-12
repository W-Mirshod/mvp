import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsTokenValid

from apps.email_analysis.serializers.email_analysis_serializers import EmailInputSerializer, EmailThemeSerializer, \
    EmailPersonalizationInputSerializer
from apps.email_analysis.services.ai_functions import (
    classify_email, personalize_email, fix_grammar, summarize_email,
    generate_subject, analyze_sentiment, generate_signature, generate_email
)

logger = logging.getLogger(__name__)


class SpamDetectionView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Detect if an email is spam",
        operation_description="Detect if email is spam.\nLog the detection process.\nReturn a boolean flag.",
        request_body=EmailInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            logger.info(f"Processing spam detection for email")
            is_spam = classify_email(email_body)
            logger.info(f"Spam detection completed. Result: {is_spam}")
            return Response({"is_spam": is_spam}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Spam detection failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)


class EmailPersonalizationView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Personalize an email based on a given theme",
        operation_description="Personalize email content.\nEnhance tone and style.\nReturn a customized email.",
        request_body=EmailPersonalizationInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailPersonalizationInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email_body = serializer.validated_data["email_body"]
            theme = serializer.validated_data["theme"]

            logger.info(f"Processing email personalization with theme: {theme}")
            personalized_email = personalize_email(email_body, theme)
            logger.info("Email personalization completed")
            return Response({"personalized_email": personalized_email}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Email personalization failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)


class GrammarFixerView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Fix grammar in an email",
        operation_description="Detect grammatical errors.\nApply corrections.\nReturn the corrected email.",
        request_body=EmailInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            logger.info("Processing grammar correction")
            corrected_email = fix_grammar(email_body)
            logger.info("Grammar correction completed")
            return Response({"corrected_email": corrected_email}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Grammar correction failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)


class EmailSummarizationView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Summarize an email",
        operation_description="Extract key ideas from email.\nCondense information effectively.\nReturn a summary string.",
        request_body=EmailInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            logger.info("Processing email summarization")
            summary = summarize_email(email_body)
            logger.info("Email summarization completed")
            return Response({"summary": summary}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Email summarization failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)


class SubjectLineGeneratorView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Generate subject lines for an email",
        operation_description="Analyze email content.\nDetermine suitable subject lines.\nReturn subject suggestions.",
        request_body=EmailInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            logger.info("Processing subject line generation")
            subjects = generate_subject(email_body)
            logger.info("Subject line generation completed")
            return Response({"subject_suggestions": subjects}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Subject line generation failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)


class SentimentAnalysisView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Analyze the sentiment of an email",
        operation_description="Examine emotional tone.\nCompute sentiment score.\nReturn sentiment classification.",
        request_body=EmailInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            logger.info("Processing sentiment analysis")
            sentiment = analyze_sentiment(email_body)
            logger.info(f"Sentiment analysis completed. Result: {sentiment}")
            return Response({"sentiment": sentiment}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Sentiment analysis failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)


class SignatureGeneratorView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Generate an email signature",
        operation_description="Determine appropriate signature style.\nCompose signature text.\nReturn generated signature.",
        request_body=EmailInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            logger.info("Processing signature generation")
            signature = generate_signature(email_body)
            logger.info("Signature generation completed")
            return Response({"signature": signature}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Signature generation failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)


class EmailGenerationView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Generate an email based on a theme",
        operation_description="Utilize theme to create email content.\nApply creative text generation.\nReturn the generated email.",
        request_body=EmailThemeSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailThemeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            theme = serializer.validated_data["theme"]

            logger.info(f"Processing email generation with theme: {theme}")
            generated_email = generate_email(theme)
            logger.info("Email generation completed")
            return Response({"generated_email": generated_email}, status=status.HTTP_200_OK)

        except APIException as e:
            logger.error(f"Email generation failed: {str(e)}")
            return Response({"error": str(e)}, status=e.status_code)
        