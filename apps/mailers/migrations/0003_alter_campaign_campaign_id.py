# Generated by Django 5.0.6 on 2025-02-10 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailers", "0002_alter_campaign_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="campaign",
            name="campaign_id",
            field=models.CharField(
                blank=True,
                help_text="Campaign it",
                max_length=255,
                null=True,
                verbose_name="Campaign id",
            ),
        ),
    ]
