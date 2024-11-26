from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


# Create your models here.
class Country(models.Model):
    history = HistoricalRecords()

    code = models.CharField(
        max_length=3,
        primary_key=True,
        db_index=True,
        unique=True,
        verbose_name=_("Country Code"),
    )
    name = models.CharField(max_length=100, verbose_name=_("Country Name"))

    def __str__(self):
        return self.name or self.code

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ["name"]


class Nationality(models.Model):
    history = HistoricalRecords()

    nationality_name = models.CharField(
        max_length=100, verbose_name=_("Nationality Name")
    )

    def __str__(self):
        return self.nationality_name

    class Meta:
        verbose_name = _("Nationality")
        verbose_name_plural = _("Nationalities")
        ordering = ["nationality_name"]


class DegreeChoices(models.Model):
    history = HistoricalRecords()
    degree = models.CharField(
        max_length=255,
        verbose_name=_("Degree"),
        choices=[
            ("Bachelor", "Bachelor"),
            ("Master", "Master"),
            ("PhD", "PhD"),
            ("Diploma", "Diploma"),
        ],
        help_text=_("Enter the degree obtained (e.g., Bachelor, Master)."),
        unique=True,
    )

    def __str__(self):
        return self.degree

    class Meta:
        verbose_name = _("Degree")
        verbose_name_plural = _("Degrees")
        ordering = ["degree"]


class FieldOfStudy(models.Model):
    history = HistoricalRecords()
    field_of_study = models.CharField(
        max_length=255,
        verbose_name=_("Field of Study"),
        help_text=_("Enter the field of study."),
    )

    def __str__(self):
        return self.field_of_study

    class Meta:
        verbose_name = _("Field of Study")
        verbose_name_plural = _("Fields of Study")
        ordering = ["field_of_study"]


class Institution(models.Model):
    history = HistoricalRecords()
    institution = models.CharField(
        max_length=255,
        verbose_name=_("Institution"),
        help_text=_("Enter the institution."),
    )
    type = models.CharField(
        max_length=255,
        choices=[("University", "University"), ("College", "college")],
        verbose_name=_("Institution Type"),
        help_text=_("Enter the type of institution."),
    )
    abbreviation = models.CharField(
        max_length=255,
        verbose_name=_("Institution Abbreviation"),
        blank=False,
        null=True,
        help_text=_("Enter the abbreviation of the institution."),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name=_("Country"),
        help_text=_("Select the country of the educational institution."),
    )

    def __str__(self):
        return r"{} , {} , {} at {}".format(
            self.abbreviation, self.type, self.institution, self.country.name
        )

    class Meta:
        verbose_name = _("Institution")
        verbose_name_plural = _("Institutions")
        ordering = ["type", "institution"]


class EducationGradeChoices(models.Model):
    history = HistoricalRecords()
    grade = models.CharField(
        max_length=255,
        verbose_name=_("Grade"),
        help_text=_("Enter the grade obtained (e.g., Excellent, Good)."),
        unique=True,
    )

    def __str__(self):
        return self.grade

    class Meta:
        verbose_name = _("Grade")
        verbose_name_plural = _("Grades")
        ordering = ["grade"]


class LanguageChoices(models.Model):
    history = HistoricalRecords()
    language = models.CharField(
        max_length=255,
        verbose_name=_("Language-Name"),
        help_text=_("Enter the language."),
        unique=True,
    )

    def __str__(self):
        return self.language

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ["language"]


class Department(models.Model):
    history = HistoricalRecords()
    abbreviation = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Abbreviation"),
        help_text=_("Enter a unique abbreviation for the department, e.g., HR, IT."),
    )
    title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("Title"),
        help_text=_(
            "Enter the official title of the department, if different from the name."
        ),
    )

    def __str__(self):
        return rf"{self.abbreviation} , {self.title}"

    class Meta:
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ["title"]


class LicenseProvider(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name=_("License Provider"),
        help_text=_("Enter the name of the license provider."),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name=_("Country"),
        help_text=_("Select the country where the license provider is located."),
    )

    def __str__(self):
        return r"{} / {}".format(self.name, self.country.name)

    class Meta:
        verbose_name = _("License Provider")
        verbose_name_plural = _("License Providers")
        ordering = ["name"]
