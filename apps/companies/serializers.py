from rest_framework import serializers

from apps.companies.models.company import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "title", "start_date", "end_date", "employees", "is_active")


class CompanyActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ("id", "is_active")
