from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from utilities.models import (
    Nationality,
    DegreeChoices,
    FieldOfStudy,
    Department,
)

from candidates.models import Candidate

class JobOpportunity(models.Model):
    job_title = models.CharField(max_length=255, verbose_name=_("Job Title"))
    job_description = models.TextField(verbose_name=_("Job Description"))
    job_department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        verbose_name=_("Job Department"),
        related_name='job_opportunities_as_department',  # Added related_name
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_("Enter the name of the company."),
        verbose_name=_("Company Name"),
    )
    minimum_years_of_experience = models.PositiveIntegerField(
        verbose_name=_("Minimum Years of Experience")
    )
    accepted_degrees = models.ManyToManyField(
        DegreeChoices,
        verbose_name=_("Accepted Degrees"),
    )
    fields_of_study = models.ManyToManyField(
        FieldOfStudy,
        verbose_name=_("Fields of Study"),
    )
    nationalities = models.ManyToManyField(
        Nationality,
        verbose_name=_("Nationalities"),
    )
    minimum_age = models.PositiveIntegerField(verbose_name=_("Minimum Age"))
    maximum_age = models.PositiveIntegerField(verbose_name=_("Maximum Age"))
    gender = models.CharField(
        choices=[("M", _("Male")), ("F", _("Female")), ("Any", _("Any"))],
        max_length=3,
        verbose_name=_("Gender"),
    )
    departments = models.ManyToManyField(
        Department,
        verbose_name=_("Required Experience Departments"),
        help_text=_("Select departments that the candidate should have experience in."),
        related_name='job_opportunities_as_required',  # Added related_name
    )
    candidates = models.ManyToManyField(
        Candidate,
        related_name='job_opportunities',
        blank=True,
        verbose_name=_("Candidates"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Job Opportunity")
        verbose_name_plural = _("Job Opportunities")
        ordering = ["-created_at"]

    def __str__(self):
        return self.job_title
