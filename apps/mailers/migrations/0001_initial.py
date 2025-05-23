# Generated by Django 5.0.6 on 2025-01-30 20:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        (
            "backend_mailer",
            "0002_remove_emailbackend_mailing_type_email_author_and_more",
        ),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Campaign",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_deleted",
                    models.BooleanField(default=False, verbose_name="Deleted"),
                ),
                (
                    "campaign_id",
                    models.CharField(
                        help_text="Campaign it",
                        max_length=255,
                        verbose_name="Campaign id",
                    ),
                ),
                (
                    "campaign_name",
                    models.CharField(
                        help_text="Campaign name",
                        max_length=500,
                        verbose_name="Campaign name",
                    ),
                ),
                (
                    "shipping_type",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "Default"), (1, "Speed"), (2, "Extra Speed")],
                        default=0,
                        help_text="Campaign shipping type",
                    ),
                ),
                (
                    "message_type",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "Default"),
                            (1, "Promotion options"),
                            (2, "Newsletter"),
                            (3, "Transactional"),
                        ],
                        default=0,
                        help_text="Campaign message type",
                    ),
                ),
                ("comment", models.TextField(help_text="Campaign comment")),
                (
                    "open_rate",
                    models.IntegerField(default=0, help_text="Campaign open rate"),
                ),
                (
                    "visitor_clicks",
                    models.IntegerField(default=0, help_text="Campaign visitor clicks"),
                ),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[
                            (0, "created"),
                            (1, "Completed"),
                            (2, "Stopped"),
                            (3, "Error"),
                            (4, "AI Mailing"),
                            (5, "Sending"),
                        ],
                        default=0,
                        help_text="Campaign status",
                    ),
                ),
                (
                    "country_tag",
                    models.CharField(
                        help_text="Country filed",
                        max_length=3,
                        verbose_name="Country filed",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="campaign_to_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        help_text="Message for campaign",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="backend_mailer.email",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
