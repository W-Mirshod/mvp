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

class SpamDetectionView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(operation_summary="Detect if an email is spam", request_body=EmailInputSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            is_spam = classify_email(email_body)
            return Response({"is_spam": is_spam}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)


class EmailPersonalizationView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(
        operation_summary="Personalize an email based on a given theme",
        request_body=EmailPersonalizationInputSerializer
    )
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailPersonalizationInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            email_body = serializer.validated_data["email_body"]
            theme = serializer.validated_data["theme"]

            personalized_email = personalize_email(email_body, theme)
            return Response({"personalized_email": personalized_email}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)


class GrammarFixerView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(operation_summary="Fix grammar in an email", request_body=EmailInputSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            corrected_email = fix_grammar(email_body)
            return Response({"corrected_email": corrected_email}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)


class EmailSummarizationView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(operation_summary="Summarize an email", request_body=EmailInputSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            summary = summarize_email(email_body)
            return Response({"summary": summary}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)


class SubjectLineGeneratorView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(operation_summary="Generate subject lines for an email", request_body=EmailInputSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            subjects = generate_subject(email_body)
            return Response({"subject_suggestions": subjects}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)


class SentimentAnalysisView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(operation_summary="Analyze the sentiment of an email", request_body=EmailInputSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            sentiment = analyze_sentiment(email_body)
            return Response({"sentiment": sentiment}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)


class SignatureGeneratorView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(operation_summary="Generate an email signature", request_body=EmailInputSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_body = serializer.validated_data["email_body"]

            signature = generate_signature(email_body)
            return Response({"signature": signature}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)


class EmailGenerationView(APIView):
    permission_classes = (
        IsAuthenticated,
        IsTokenValid,
    )
    @swagger_auto_schema(operation_summary="Generate an email based on a theme", request_body=EmailThemeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            serializer = EmailThemeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            theme = serializer.validated_data["theme"]

            generated_email = generate_email(theme)
            return Response({"generated_email": generated_email}, status=status.HTTP_200_OK)

        except APIException as e:
            return Response({"error": str(e)}, status=e.status_code)
