from django import forms
from django.utils.translation import gettext_lazy as _
from .models import JobOpportunity

class JobOpportunityForm(forms.ModelForm):
    class Meta:
        model = JobOpportunity
        fields = [
            'job_title',
            'job_description',
            'job_department',
            'company_name',
            'minimum_years_of_experience',
            'accepted_degrees',
            'fields_of_study',
            'nationalities',
            'minimum_age',
            'maximum_age',
            'gender',
            'departments',
        ]
        widgets = {

        }
