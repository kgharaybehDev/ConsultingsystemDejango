from django.contrib import admin
from .models import JobOpportunity

@admin.register(JobOpportunity)
class JobOpportunityAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'job_department', 'company_name', 'created_at')
    search_fields = ('job_title', 'company_name')
    list_filter = ('job_department', 'gender')
    filter_horizontal = (
        'accepted_degrees',
        'fields_of_study',
        'nationalities',
        'departments',
        'candidates',
    )
