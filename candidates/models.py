import os
import re
from audioop import reverse
from datetime import date
from dateutil.relativedelta import relativedelta
from django_ckeditor_5.fields import CKEditor5Field


from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from simple_history.models import HistoricalRecords

from utilities.models import (
    Nationality,
    Country,
    Institution,
    DegreeChoices,
    FieldOfStudy,
    EducationGradeChoices,
    Department,
    LanguageChoices,
    LicenseProvider,
)

# Constants
PHONE_REGEX = r"^\+[1-9]\d{1,14}$"


# Validators
def validate_phone_number(value):
    if not re.match(PHONE_REGEX, value):
        raise ValidationError(
            _('Phone number must start with "+" followed by country code and number.')
        )


def validate_end_date_after_start(start_date, end_date):
    if end_date and end_date < start_date:
        raise ValidationError(_("End date cannot be before start date."))


# Helper Functions
def get_candidate_directory(instance):
    full_name = instance.full_name
    sanitized_full_name = re.sub(r"[^\w\s-]", "", full_name).strip().lower()
    sanitized_full_name = re.sub(r"[-\s]+", "-", sanitized_full_name)
    return f"candidates/{sanitized_full_name}_{instance.pk}"


def profile_image_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"profile_image.{ext}"
    candidate_directory = get_candidate_directory(instance)
    return os.path.join(candidate_directory, "images", filename)


def id_copy_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"national_id_copy.{ext}"
    candidate_directory = get_candidate_directory(instance)
    return f"{candidate_directory}/{filename}"


def passport_copy_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"PASS.{ext}"
    candidate_directory = get_candidate_directory(instance)
    return f"{candidate_directory}/{filename}"


def resume_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"resume.{ext}"
    candidate_directory = get_candidate_directory(instance)
    return f"{candidate_directory}/{filename}"


def education_certification_upload_path(instance, filename):
    # Split to get the file extension
    ext = filename.split(".")[-1]
    degree_prefix = {
        "Diploma": "DIc",
        "Bachelor": "BCc",
        "Master": "MSc",
        "PhD": "PhDc",
    }
    degree = instance.degree.degree.strip().capitalize() if instance.degree else ""
    prefix = degree_prefix.get(degree, "education_certification")

    filename = f"{prefix}{instance.candidate.educations.count()}.{ext}"


    candidate_directory = get_candidate_directory(instance.candidate)

    return f"{candidate_directory}/{filename}"


def education_transcript_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    degree_prefix = {
        "Diploma": "DIt",
        "Bachelor": "BCt",
        "Master": "MSt",
        "PhD": "PhDt",
    }



    degree = instance.degree.degree.strip().capitalize() if instance.degree else ""
    prefix = degree_prefix.get(degree, "education_transcript")


    filename = f"{prefix}{instance.candidate.educations.count()}.{ext}"

    candidate_directory = get_candidate_directory(instance.candidate)

    return f"{candidate_directory}/{filename}"


def experience_certification_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"EXP{instance.candidate.experiences.count()}.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def training_course_certification_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"course{instance.pk}.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def license_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    license_country = instance.license_provider.country.code or "N/A"
    filename = f"{license_country}_Lic.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_prometric_appointments(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"prometric_appointment.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_dataflow_certificates(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"Dflow.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_dhp_certificates(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"dhpCV.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_police_clearance(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"PCC.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_prometric_certificates(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"Promi.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_blood_test_report(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"blood_test_report.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/medical_tests/{filename}"


def candidate_xray_test_report(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"xray_test_report.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_pregnancy_report(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"pregnancy_report.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_fit_to_work_report(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"fit_to_work_report.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


def candidate_visa_certificates(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"visa.{ext}"
    candidate_directory = get_candidate_directory(instance.candidate)
    return f"{candidate_directory}/{filename}"


# Models
class Candidate(models.Model):
    # pk = models.pkField(default=pk.pk4, editable=False, unique=True)
    is_open_to_work = models.CharField(
        choices=[("Yes", _("Yes")), ("NO", _("No"))],
        max_length=5,
        verbose_name=_("Open to Work"),
    )
    # Personal Information
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("First Name"),
    )
    second_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Second Name"),
    )
    third_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Third Name"),
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name=_("Last Name"),
    )
    gender = models.CharField(
        choices=[("M", _("Male")), ("F", _("Female"))],
        max_length=1,
        verbose_name=_("Gender"),
    )
    birthday = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Birthday"),
    )

    nationality = models.ForeignKey(
        Nationality,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name=_("Nationality"),
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        blank=False,
        null=True,
        verbose_name=_("Country"),
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Address"),
    )

    # Contact Information
    call_phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("Call Phone Number"),
        validators=[validate_phone_number],
    )
    whatsapp_phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("WhatsApp Phone Number"),
        validators=[validate_phone_number],
    )

    # Document Uploads
    personal_image = models.ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Personal Image"),
        max_length=500,
    )
    national_id_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("National ID Number"),
    )
    national_id_copy = models.FileField(
        upload_to=id_copy_upload_path,
        blank=True,
        null=True,
        verbose_name=_("National ID Copy"),
    )
    passport_copy = models.FileField(
        upload_to=passport_copy_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Passport Copy"),
    )
    passport_expiration_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Passport Expiration Date"),
    )
    passport_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Passport ID"),
    )
    resume_copy = models.FileField(
        upload_to=resume_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Resume Copy"),
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _("Candidate")
        verbose_name_plural = _("Candidates")
        ordering = ["-created_at"]

    @property
    def full_name(self):
        names = [
            self.first_name,
            self.second_name,
            self.third_name,
            self.last_name,
        ]
        return " ".join(filter(None, names))

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def get_total_experience_years_based_on_departments(self, departments=None):
        total_months = 0
        experiences = self.experiences.all()

        if departments:
            # Filter experiences that include any of the specified departments
            experiences = experiences.filter(departments__in=departments).distinct()

        for experience in experiences:
            start_date = experience.start_date
            end_date = experience.end_date or date.today()
            delta = relativedelta(end_date, start_date)
            months = delta.years * 12 + delta.months
            total_months += months

        total_years = total_months / 12.0
        return total_years

    @property
    def age_in_years(self):
        if self.birthday:
            today = date.today()
            age = relativedelta(today, self.birthday)
            return age.years
        return None

    def clean(self):
        super().clean()
        if self.first_name is not None:
            self.first_name = self.first_name.strip().capitalize()
        if self.second_name is not None:
            self.second_name = self.second_name.strip().capitalize()
        if self.third_name is not None:
            self.third_name = self.third_name.strip().capitalize()
        if self.last_name is not None:
            self.last_name = self.last_name.strip().capitalize()


    def profile_completeness(self):
        required_fields = [
            "first_name",
            "second_name",
            "third_name",
            "last_name",
            "birthday",
            "nationality",
            "address",
            "personal_image",
            "national_id_number",
            "national_id_copy",  # Optional field
            "passport_copy",
            "passport_expiration_date",
            "passport_id",
            "call_phone_number",
            "whatsapp_phone_number",  # Optional field
        ]
        filled_fields = [field for field in required_fields if getattr(self, field)]
        return len(filled_fields) / len(required_fields) * 100

    def delete_resume(self):
        if self.resume_copy:
            print("Deleting resume")
            self.resume_copy.delete(save=False)
            self.resume_copy = None
            self.save()

    def delete_image(self):
        if self.personal_image:
            try:
                print("Deleting image")
                self.personal_image.delete(save=False)
                self.personal_image = None
                self.save()
            except Exception as e:
                print(f"Failed to delete image: {e}")
                raise

    def delete_id_copy(self):
        if self.national_id_copy:
            print("Deleting id copy")
            self.national_id_copy.delete(save=False)
            self.national_id_copy = None
            self.save()

    def delete_passport_copy(self):
        if self.passport_copy:
            print("Deleting passport copy")
            self.passport_copy.delete(save=False)
            self.passport_copy = None
            self.save()

    def candidate_age(self):
        if self.birthday:
            today = date.today()
            age = relativedelta(today, self.birthday)
            return age

    def candidate_age_str(self):
        if self.birthday:
            today = date.today()
            age = relativedelta(today, self.birthday)
            return f"{age.years} years, {age.months} months"

    def total_experience(self):
        total_years = 0
        total_months = 0

        for experience in self.experiences.all():
            start_date = experience.start_date
            end_date = experience.end_date if experience.end_date else date.today()
            delta = relativedelta(end_date, start_date)
            total_years += delta.years
            total_months += delta.months

        # Adjust months to convert into full years if needed
        total_years += total_months // 12
        total_months = total_months % 12

        return "{} years, {} months".format(total_years, total_months)

    def departments(self):

        departments = set()
        for experience in self.experiences.all():
            for department in experience.departments.all():

                departments.add(department.abbreviation)

        if len(departments) == 0:
            return "N/A"

        return ", ".join(departments)

    def age(self):
        if self.birthday:
            today = date.today()
            age = relativedelta(today, self.birthday)
            return r"{} years, {} months".format(age.years, age.months)

    def get_total_experience_years(self):
        total_months = 0
        experiences = self.experiences.all()

        for experience in experiences:
            start_date = experience.start_date
            end_date = experience.end_date or date.today()
            delta = relativedelta(end_date, start_date)
            months = delta.years * 12 + delta.months
            total_months += months

        total_years = total_months / 12.0
        return total_years

class Education(models.Model):
    history = HistoricalRecords()

    # Candidate Information
    candidate = models.ForeignKey(
        Candidate,
        related_name="educations",
        on_delete=models.CASCADE,
        verbose_name=_("Candidate"),
        help_text=_("Select the candidate for this education."),
    )

    # Education Information
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        null=True,
        verbose_name=_("Institution"),
        help_text=_("Select the institution."),
    )

    degree = models.ForeignKey(
        DegreeChoices,
        on_delete=models.PROTECT,
        verbose_name=_("Degree"),
        help_text=_("Select the degree obtained (e.g., Bachelor, Master)."),
    )
    field_of_study = models.ForeignKey(
        FieldOfStudy,
        on_delete=models.PROTECT,
        verbose_name=_("Field of Study"),
        help_text=_("Select the field of study."),
    )
    start_date = models.DateField(
        verbose_name=_("Start Date"),
        help_text=_("Enter the start date of the education."),
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("End Date"),
        help_text=_("Enter the end date of the education, if applicable."),
    )
    online = models.BooleanField(
        default=False,
        verbose_name=_("Online"),
        help_text=_("Check if the education was taken online."),
    )
    gpa = models.FloatField(
        blank=True,
        null=True,
        verbose_name=_("GPA"),
        help_text=_("Enter the GPA obtained (e.g., 3.5)."),
    )
    grade = models.ForeignKey(
        EducationGradeChoices,
        on_delete=models.PROTECT,
        verbose_name=_("Grade"),
        help_text=_("Select the grade obtained (e.g., A, B+)."),
        null=True,
        blank=True,
    )
    certification_copy = models.FileField(
        upload_to=education_certification_upload_path,
        blank=True,
        null=False,
        verbose_name=_("Certification Copy"),
        help_text=_(
            "Upload a copy of the certification obtained during this education."
        ),
    )
    transcript_copy = models.FileField(
        upload_to=education_transcript_upload_path,
        blank=True,
        null=False,
        verbose_name=_("Transcript Copy"),
        help_text=_("Upload a copy of the transcript for this education."),
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when this record was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when this record was last updated."),
    )

    def delete_certification_copy(self):
        if self.certification_copy:
            self.certification_copy.delete(save=False)
            self.certification_copy = None
            self.save()

    def delete_transcript_copy(self):
        if self.transcript_copy:
            self.transcript_copy.delete(save=False)
            self.transcript_copy = None
            self.save()

    def clean(self):
        super().clean()
        validate_end_date_after_start(self.start_date, self.end_date)

    def get_duration(self):
        if self.end_date:
            return f"{self.start_date} - {self.end_date}"
        else:
            return f"{self.start_date} - Present"

    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Educations")
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date"))
                | models.Q(end_date__isnull=True),
                name="education_end_date_after_start_date",
            )
        ]


class Experience(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        related_name="experiences",
        on_delete=models.CASCADE,
        verbose_name=_("Candidate"),
        help_text=_("Select the candidate for this experience."),
    )
    # Company Information
    company_name = models.CharField(
        max_length=255,
        verbose_name=_("Company Name"),
        help_text=_("Enter the name of the company."),
    )
    company_location = CountryField(
        verbose_name=_("Company Location"),
        help_text=_("Enter the location of the company."),
    )
    # Reference Information
    reference_name = models.CharField(
        max_length=255,
        verbose_name=_("Reference Name"),
        help_text=_("Enter the name of the reference person, such as HR or Manager."),
        blank=True,
        null=True,
    )
    reference_job_title = models.CharField(
        max_length=255,
        verbose_name=_("Reference Job Title"),
        help_text=_("Enter the job title of the reference person."),
        blank=True,
        null=True,
    )
    reference_contact_info = models.CharField(
        max_length=255,
        verbose_name=_("Reference Contact Information"),
        help_text=_(
            "Enter the contact details (phone or email) of the reference person."
        ),
        blank=True,
        null=True,
    )
    # Job Information
    job_title = models.CharField(
        max_length=255,
        verbose_name=_("Job Title"),
        help_text=_("Enter the job title for this experience."),
    )
    departments = models.ManyToManyField(
        Department,
        verbose_name=_("Departments"),
    )
    # Date Information
    start_date = models.DateField(
        verbose_name=_("Start Date"),
        help_text=_("Enter the start date of the experience."),
    )
    end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("End Date"),
        help_text=_("Enter the end date of the experience, if applicable."),
    )
    # Additional Information
    job_responsibilities = CKEditor5Field( config_name='extends', 
        verbose_name=_("Job Responsibilities"),
        help_text=_("Enter the job responsibilities."),
        blank=True,
        null=True,
    )
    certification_copy = models.FileField(
        upload_to=experience_certification_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Certification Copy"),
        help_text=_(
            "Upload a copy of any certifications obtained during this experience."
        ),
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when this record was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when this record was last updated."),
    )

    history = HistoricalRecords()

    def __str__(self):
        return f"{self.company_name} - {self.job_title}"

    def get_company_location(self):
        return self.company_location.name

    def delete_certification_copy(self):
        if self.certification_copy:
            self.certification_copy.delete(save=False)
            self.certification_copy = None
            self.save()

    def clean(self):
        super().clean()
        validate_end_date_after_start(self.start_date, self.end_date)

    def get_duration(self):
        """
        Calculate and return the duration of the experience.

        :return: str - Duration in the format "X Years, Y Months"
        """
        # If the experience is still ongoing
        if self.end_date is None:
            end_date = date.today()
        else:
            end_date = self.end_date

        # Calculate the difference using relativedelta
        duration = relativedelta(end_date, self.start_date)

        # Format duration into "X Years, Y Months"
        years = duration.years
        months = duration.months

        # Constructing the duration string
        duration_parts = []
        if years > 0:
            duration_parts.append(f"{years} Year{'s' if years > 1 else ''}")
        if months > 0:
            duration_parts.append(f"{months} Month{'s' if months > 1 else ''}")

        return ", ".join(duration_parts) if duration_parts else "Less than a month"

    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experiences")
        ordering = ["-start_date"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date"))
                | models.Q(end_date__isnull=True),
                name="experience_end_date_after_start_date",
            )
        ]


class Language(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        related_name="languages",
        on_delete=models.CASCADE,
        verbose_name=_("Candidate"),
        help_text=_("Select the candidate for this language."),
    )
    language = models.ForeignKey(
        LanguageChoices,
        on_delete=models.PROTECT,
        verbose_name=_("Language"),
        related_name="languages",
        help_text=_("Select the language."),
    )

    class Meta:
        verbose_name = _("Language")
        verbose_name_plural = _("Languages")
        ordering = ["language"]

    def __str__(self):
        return f"{self.language}"


class TrainingCourse(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name="training_courses",
        verbose_name=_("Candidate"),
        help_text=_("Select the candidate associated with this training course."),
    )
    course_name = models.CharField(
        max_length=255,
        verbose_name=_("Course Name"),
        help_text=_(
            "Enter the title of the training course (e.g., Advanced Python Programming)."
        ),
    )
    institution = models.CharField(
        max_length=255,
        verbose_name=_("Institution"),
        help_text=_("Enter the name of the institution providing the training course."),
    )
    location = CountryField(
        blank=True,
        null=True,
        verbose_name=_("Location"),
        help_text=_("Enter the country where the training course was held."),
    )
    start_date = models.DateField(
        verbose_name=_("Start Date"),
        help_text=_("Enter the start date of the training course."),
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("End Date"),
        help_text=_(
            "Enter the end date of the training course. Leave blank if ongoing."
        ),
    )
    description = CKEditor5Field( config_name='extends', 
        blank=True,
        null=True,
        verbose_name=_("Description"),
        help_text=_(
            "Provide additional details about the course, such as the subjects covered or skills acquired."
        ),
    )
    certification_copy = models.FileField(
        upload_to=training_course_certification_upload_path,
        blank=True,
        null=True,
        verbose_name=_("Certification Copy"),
        help_text=_("Upload the certification copy, if available."),
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when this record was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when this record was last updated."),
    )
    history = HistoricalRecords()

    def clean(self):
        super().clean()
        validate_end_date_after_start(self.start_date, self.end_date)

    def delete_certification_copy(self):
        if self.certification_copy:
            self.certification_copy.delete(save=False)
            self.certification_copy = None
            self.save()

    class Meta:
        verbose_name = _("Training Course")
        verbose_name_plural = _("Training Courses")
        ordering = ["-start_date"]
        unique_together = ("candidate", "course_name", "start_date")
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gte=models.F("start_date"))
                | models.Q(end_date__isnull=True),
                name="training_course_end_date_after_start_date",
            )
        ]


class License(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        related_name="licenses",
        on_delete=models.CASCADE,
        verbose_name=_("Candidate"),
        help_text=_("Select the candidate associated with this license."),
    )
    license_name = models.CharField(
        max_length=255,
        verbose_name=_("License Name"),
        help_text=_(
            "Enter the name of the license (e.g., Driving License, Medical License)."
        ),
        default="Nursing",
    )
    license_number = models.CharField(
        max_length=100,
        verbose_name=_("License Number"),
        help_text=_("Enter the unique license number."),
    )

    license_provider = models.ForeignKey(
        LicenseProvider,
        on_delete=models.PROTECT,
        verbose_name=_("License Provider"),
        help_text=_("Select the organization or provider issuing the license."),
    )
    issued_date = models.DateField(
        verbose_name=_("Issued Date"),
        help_text=_("Enter the date when the license was issued."),
    )
    expiry_date = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Expiry Date"),
        help_text=_(
            "Enter the expiry date of the license, if applicable. Leave blank if the license doesn't expire."
        ),
    )
    license_copy = models.FileField(
        upload_to=license_upload_path,
        blank=True,
        null=True,
        verbose_name=_("License Copy"),
        help_text=_("Upload a scanned copy of the license (optional)."),
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At"),
        help_text=_("The date and time when this record was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time when this record was last updated."),
    )
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.license_name} ({self.license_number})"

    def is_expired(self):
        """Returns True if the license has expired."""
        return self.expiry_date is not None and date.today() > self.expiry_date

    def delete_license_copy(self):
        """Deletes the license copy associated with this license."""
        if self.license_copy:
            self.license_copy.delete(save=False)
            self.license_copy = None
            self.save()

    def clean(self):
        """Custom validation to ensure that the expiry date is not before the issued date."""
        super().clean()
        if self.expiry_date and self.expiry_date < self.issued_date:
            raise ValidationError(
                _("Expiry date cannot be earlier than the issued date.")
            )

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")
        ordering = ["-issued_date"]
        unique_together = (
            "candidate",
            "license_number",
        )  # Ensures a candidate doesn't have duplicate license numbers


class CandidateApplicationData(models.Model):
    candidate = models.OneToOneField(
        Candidate,
        on_delete=models.CASCADE,
        related_name="application_data",
        verbose_name=_("Candidate"),
    )
    is_candidate_start_work = models.BooleanField(
        default=False,
        verbose_name=_("Is Candidate Start Work?"),
        help_text=_("Is the candidate starting work?"),
    )
    follow_up_assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_candidates",
        verbose_name=_("Follow Up Assigned To"),
    )
    history = HistoricalRecords()

    HMC_Portal_email = models.EmailField(
        verbose_name=_("HMC Portal Email"),
        blank=True,
        null=True,
    )
    HMC_Portal_password = models.CharField(
        max_length=50,
        verbose_name=_("HMC Portal Password"),
        blank=True,
        null=True,
    )
    JOB_OFFER_ID = models.CharField(
        max_length=50,
        verbose_name=_("JOB OFFER ID"),
        blank=True,
        null=True,
    )

    # DataFlow Fields
    DataFlow_issue_date = models.DateField(
        verbose_name=_("Issue Date"), null=True, blank=True
    )
    DataFlow_expiry_date = models.DateField(
        verbose_name=_("Expiry Date"), null=True, blank=True
    )

    DataFlow_case_number = models.CharField(
        max_length=100, verbose_name=_("Case Number"), null=True, blank=True
    )
    DataFlow_passport_number = models.CharField(
        max_length=50, verbose_name=_("Passport Number"), null=True, blank=True
    )
    DataFlow_is_paid = models.BooleanField(
        default=False, verbose_name=_("Is Paid"), null=True, blank=True
    )
    DataFlow_certificate_copy = models.FileField(
        upload_to=candidate_dataflow_certificates,
        verbose_name=_("DataFlow Certificate Copy"),
        null=True,
        blank=True,
    )

    # DHP Fields
    DHP_email = models.EmailField(verbose_name=_("Email"), null=True, blank=True)
    DHP_number = models.CharField(
        max_length=50, verbose_name=_("DHP Number"), null=True, blank=True
    )
    DHP_Password = models.CharField(
        max_length=50,
        verbose_name=_("DHP Password"),
        null=True,
        blank=True,
    )
    DHP_issue_date = models.DateField(
        verbose_name=_("Issue Date"), null=True, blank=True
    )
    DHP_expiry_date = models.DateField(
        verbose_name=_("Expiry Date"), null=True, blank=True
    )
    DHP_copy = models.FileField(
        upload_to=candidate_dhp_certificates,
        help_text="DHP certificate",
        verbose_name=_("DHP Certificate Copy"),
        null=True,
        blank=True,
    )
    DHP_note = CKEditor5Field( config_name='extends', blank=True, null=True, verbose_name=_("Note"))
    is_dataflow = models.BooleanField(
        default=False, verbose_name=_("Is Dataflow Candidate"), null=True, blank=True
    )
    is_Prometric = models.BooleanField(
        default=False, verbose_name=_("Is Prometric Candidate"), null=True, blank=True
    )
    is_completed_payment = models.BooleanField(
        default=False, verbose_name=_("Is Complete Payment"), null=True, blank=True
    )

    # Police Clearance Certificate Fields
    PCC_issue_date = models.DateField(
        verbose_name=_("Issue Date"), null=True, blank=True
    )
    PCC_is_stamp = models.BooleanField(
        default=False, verbose_name=_("Is Stamped"), null=True, blank=True
    )
    PCC_clearance_copy = models.FileField(
        upload_to=candidate_police_clearance,
        verbose_name=_("Police Clearance Certificate Copy"),
        null=True,
        blank=True,
    )
    PCC_expiry_date = models.DateField(
        verbose_name=_("Expiry Date"), null=True, blank=True
    )

    # Prometric Fields
    Prometric_issue_date = models.DateField(
        verbose_name=_("Issue Date"), null=True, blank=True
    )
    Prometric_Appointment_copy = models.FileField(
        upload_to=candidate_prometric_appointments,
        verbose_name=_("Prometric Appointment Copy"),
        null=True,
        blank=True,
    )
    Prometric_expiry_date = models.DateField(
        verbose_name=_("Expiry Date"), null=True, blank=True
    )
    Prometric_status = models.CharField(
        choices=[
            ("undertaken", _("Undertaken")),
            ("pass", _("Pass")),
            ("fail", _("Fail")),
        ],
        max_length=20,
        verbose_name=_("Status"),
        null=True,
        blank=True,
    )
    Prometric_certificate_copy = models.FileField(
        upload_to=candidate_prometric_certificates,
        verbose_name=_("Prometric Certificate Copy"),
        null=True,
        blank=True,
    )

    # Medical Test Fields
    MedicalTest_blood_test = models.BooleanField(
        verbose_name=_("Blood Test"), null=True, blank=True
    )
    MedicalTest_blood_test_report = models.FileField(
        upload_to=candidate_blood_test_report,
        blank=True,
        null=True,
        verbose_name=_("Blood Test Report Copy"),
    )
    MedicalTest_xray_test = models.BooleanField(
        verbose_name=_("X-Ray Test"), null=True, blank=True
    )
    MedicalTest_xray_test_report = models.FileField(
        upload_to=candidate_xray_test_report,
        blank=True,
        null=True,
        verbose_name=_("X-Ray Test Report Copy"),
    )
    MedicalTest_is_pregnant = models.BooleanField(
        verbose_name=_("Is Pregnant"), null=True, blank=True
    )
    MedicalTest_pregnancy_report = models.FileField(
        upload_to=candidate_pregnancy_report,
        blank=True,
        null=True,
        verbose_name=_("Pregnancy Report Copy"),
    )
    MedicalTest_pregnancy_month = models.IntegerField(
        verbose_name=_("How many months"), null=True, blank=True
    )
    MedicalTest_is_fit_to_work = models.BooleanField(
        verbose_name=_("Fit to Work"), null=True, blank=True
    )
    MedicalTest_fit_to_work_report = models.FileField(
        upload_to=candidate_fit_to_work_report,
        blank=True,
        null=True,
        verbose_name=_("Fit to Work Report Copy"),
    )

    # Travel Details Fields
    TravelDetails_departure_date = models.DateField(
        verbose_name=_("Departure Date"), null=True, blank=True
    )
    TravelDetails_airport = models.CharField(
        max_length=100, verbose_name=_("Airport"), null=True, blank=True
    )
    TravelDetails_note = CKEditor5Field( config_name='extends', blank=True, null=True, verbose_name=_("Note"))

    # Visa Fields
    Visa_issue_date = models.DateField(
        verbose_name=_("Issue Date"), blank=True, null=True
    )
    Visa_expiry_date = models.DateField(
        verbose_name=_("Expiry Date"), blank=True, null=True
    )
    Visa_status = models.CharField(
        choices=[
            ("undertaken", _("Undertaken")),
            ("pass", _("Pass")),
            ("fail", _("Fail")),
        ],
        max_length=20,
        verbose_name=_("Status"),
        blank=True,
        null=True,
    )
    Visa_copy = models.FileField(
        upload_to=candidate_visa_certificates,
        verbose_name=_("Visa Certificate Copy"),
        blank=True,
        null=True,
    )

    # Delete methods for specific file fields
    # Delete methods for specific file fields
    def delete_blood_test_report(self):
        """Deletes the blood test report file from storage."""
        if self.MedicalTest_blood_test_report:
            self.MedicalTest_blood_test_report.delete(save=False)
            self.MedicalTest_blood_test_report = None
            self.save()

    def delete_xray_test_report(self):
        """Deletes the X-ray test report file from storage."""
        if self.MedicalTest_xray_test_report:
            self.MedicalTest_xray_test_report.delete(save=False)
            self.MedicalTest_xray_test_report = None
            self.save()

    def delete_fit_to_work_report(self):
        """Deletes the fit to work report file from storage."""
        if self.MedicalTest_fit_to_work_report:
            self.MedicalTest_fit_to_work_report.delete(save=False)
            self.MedicalTest_fit_to_work_report = None
            self.save()

    def delete_pregnancy_report(self):
        """Deletes the pregnancy report file from storage."""
        if self.MedicalTest_pregnancy_report:
            self.MedicalTest_pregnancy_report.delete(save=False)
            self.MedicalTest_pregnancy_report = None
            self.save()

    def delete_dhp_certificate(self):
        """Deletes the DHP certificate copy from storage."""
        if self.DHP_copy:
            self.DHP_copy.delete(save=False)
            self.DHP_copy = None
            self.save()

    def delete_prometric_certificate(self):
        """Deletes the Prometric certificate copy from storage."""
        try:
            if self.Prometric_certificate_copy:
                self.Prometric_certificate_copy.delete(save=False)
                self.Prometric_certificate_copy = None
                self.save()
        except Exception as e:
            print(f"Failed to delete Prometric certificate: {e}")

    def delete_police_clearance_copy(self):
        """Deletes the Police Clearance Certificate from storage."""
        if self.PCC_clearance_copy:
            self.PCC_clearance_copy.delete(save=False)
            self.PCC_clearance_copy = None
            self.save()

    def delete_visa_copy(self):
        """Deletes the Visa certificate copy from storage."""
        if self.Visa_copy:
            self.Visa_copy.delete(save=False)
            self.Visa_copy = None
            self.save()

    def delete_dataflow_certificate_copy(self):
        """Deletes the DataFlow certificate copy from storage."""
        if self.DataFlow_certificate_copy:
            self.DataFlow_certificate_copy.delete(save=False)
            self.DataFlow_certificate_copy = None
            self.save()

    def delete_prometric_appointment_copy(self):
        """Deletes the Prometric Appointment copy from storage."""
        if self.Prometric_Appointment_copy:
            self.Prometric_Appointment_copy.delete(save=False)
            self.Prometric_Appointment_copy = None
            self.save()

    def __str__(self):
        return f"Candidate Data for {self.candidate.full_name}"

    class Meta:
        verbose_name = _("Candidate Data")
        verbose_name_plural = _("Candidates Data")
