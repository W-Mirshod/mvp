from django.contrib import admin

from apps.companies.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'start_date', 'end_date', 'is_deleted')
    list_filter = ('is_deleted', 'start_date', 'end_date')
    search_fields = ('title',)
    filter_horizontal = ('employees',)
