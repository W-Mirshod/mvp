from django.urls import path

from apps.email_analysis.views.v1.views_email_analysis import (
    SpamDetectionView,
    EmailPersonalizationView,
    GrammarFixerView,
    EmailSummarizationView,
    SubjectLineGeneratorView,
    SentimentAnalysisView,
    SignatureGeneratorView,
    EmailGenerationView,
)

app_name = "email_analysis_api"

urlpatterns = [
    path("spam-detection/", SpamDetectionView.as_view(), name="spam_detection"),
    path("email-personalization/", EmailPersonalizationView.as_view(), name="email_personalization"),
    path("grammar-fixer/", GrammarFixerView.as_view(), name="grammar_fixer"),
    path("email-summarization/", EmailSummarizationView.as_view(), name="email_summarization"),
    path("subject-line-generator/", SubjectLineGeneratorView.as_view(), name="subject_line_generator"),
    path("sentiment-analysis/", SentimentAnalysisView.as_view(), name="sentiment_analysis"),
    path("signature-generator/", SignatureGeneratorView.as_view(), name="signature_generator"),
    path("email-generation/", EmailGenerationView.as_view(), name="email_generation"),
]
