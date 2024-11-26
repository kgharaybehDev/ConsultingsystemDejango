# candidates/forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget

from .models import (
    Candidate,
    Education,
    Experience,
    Language,
    TrainingCourse,
    CandidateApplicationData,
    License,
)


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = [
            "email",
            "first_name",
            "second_name",
            "third_name",
            "last_name",
            "gender",
            "birthday",
            "nationality",
            "country",
            "address",
            "call_phone_number",
            "whatsapp_phone_number",
            "personal_image",
            "national_id_number",
            "national_id_copy",
            "passport_copy",
            "passport_expiration_date",
            "passport_id",
            "resume_copy",
            "is_open_to_work",
        ]
        widgets = {
            "birthday": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "passport_expiration_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "nationality": forms.Select(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "personal_image": forms.FileInput(attrs={"class": "form-control"}),
            "national_id_copy": forms.FileInput(attrs={"class": "form-control"}),
            "passport_copy": forms.FileInput(attrs={"class": "form-control"}),
            "resume_copy": forms.FileInput(attrs={"class": "form-control"}),
            "is_open_to_work": forms.Select(attrs={"class": "form-control"}),
        }


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ["candidate"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "degree": forms.Select(attrs={"class": "form-control"}),
            "field_of_study": forms.Select(attrs={"class": "form-control"}),
            "institution": forms.Select(attrs={"class": "form-control"}),
            "grade": forms.Select(attrs={"class": "form-control"}),
            "online": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "gpa": forms.NumberInput(attrs={"class": "form-control"}),
            "certification_copy": forms.FileInput(attrs={"class": "form-control-file"}),
            "transcript_copy": forms.FileInput(attrs={"class": "form-control-file"}),
        }

    def __init__(self, *args, **kwargs):
        super(EducationForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ not in [
                forms.CheckboxInput,
                forms.FileInput,
                forms.Select,
                forms.DateInput,
            ]:
                field.widget.attrs["class"] = "form-control"


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ["candidate"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "company_location": forms.Select(attrs={"class": "form-control"}),

            "certification_copy": forms.FileInput(attrs={"class": "form-control-file"}),
            "departments": forms.SelectMultiple(
                attrs={"class": "form-control select2", "multiple": "multiple"}
            ),  # Fix


            "job_responsibilities": CKEditor5Widget(
                attrs={"class": "django_ckeditor_5"}, config_name="extends")

        }


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        exclude = ["candidate"]
        widgets = {
            "language": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ != forms.Select:
                field.widget.attrs["class"] = "form-control"


class TrainingCourseForm(forms.ModelForm):
    class Meta:
        model = TrainingCourse
        exclude = ["candidate"]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "location": forms.Select(attrs={"class": "form-control"}),
            "description":  CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              ),
            "certification_copy": forms.FileInput(attrs={"class": "form-control-file"}),
        }

    def __init__(self, *args, **kwargs):
        super(TrainingCourseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.__class__ not in [
                forms.FileInput,
                forms.Select,
                forms.DateInput,
            ]:
                field.widget.attrs["class"] = "form-control"


class LicenseForm(forms.ModelForm):
    class Meta:
        model = License
        exclude = ["candidate"]
        widgets = {
            "license_provider": forms.Select(attrs={"class": "form-control"}),
            "license_type": forms.Select(attrs={"class": "form-control"}),
            "license_number": forms.TextInput(attrs={"class": "form-control"}),
            "issued_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "expiry_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "license_copy": forms.FileInput(attrs={"class": "form-control-file"}),
        }


class CandidateApplicationDataForm(forms.ModelForm):
    class Meta:
        model = CandidateApplicationData
        exclude = ["candidate"]
        widgets = {
            # General Information
            "follow_up_assigned_to": forms.Select(attrs={"class": "form-control"}),
            "is_candidate_start_work": forms.CheckboxInput(),  # is_Candidate_Start_Work
            "HMC_Portal_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter HMC Portal Email"}
            ),
            "HMC_Portal_password": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter HMC Portal Password",
                }
            ),
            "JOB_OFFER_ID": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Job Offer ID"}
            ),
            # DataFlow Fields
            "DataFlow_issue_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "DataFlow_expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "DataFlow_case_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Case Number"}
            ),
            "DataFlow_passport_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Passport Number"}
            ),
            "DataFlow_is_paid": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "DataFlow_certificate_copy": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            # DHP Fields
            "DHP_email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Enter DHP Email"}
            ),
            "DHP_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter DHP Number"}
            ),
            "DHP_Password": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter DHP Password"}
            ),
            "DHP_issue_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "DHP_expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "DHP_copy": forms.FileInput(attrs={"class": "form-control-file"}),
            "DHP_note": CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              ),
            # General Boolean Fields
            "is_dataflow": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_Prometric": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_completed_payment": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            # Police Clearance Certificate Fields
            "PCC_issue_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "PCC_expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "PCC_is_stamp": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "PCC_clearance_copy": forms.FileInput(attrs={"class": "form-control-file"}),
            # Prometric Fields
            "Prometric_issue_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "Prometric_expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "Prometric_status": forms.Select(attrs={"class": "form-control"}),
            "Prometric_certificate_copy": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            "Prometric_Appointment_copy": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            # Medical Test Fields
            "MedicalTest_blood_test": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "MedicalTest_blood_test_report": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            "MedicalTest_xray_test": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "MedicalTest_xray_test_report": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            "MedicalTest_is_pregnant": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "MedicalTest_pregnancy_report": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            "MedicalTest_pregnancy_month": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Number of months pregnant",
                }
            ),
            "MedicalTest_is_fit_to_work": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "MedicalTest_fit_to_work_report": forms.FileInput(
                attrs={"class": "form-control-file"}
            ),
            # Travel Details Fields
            "TravelDetails_departure_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "TravelDetails_airport": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Airport"}
            ),
            "TravelDetails_note":  CKEditor5Widget(
                  attrs={"class": "django_ckeditor_5"}, config_name="extends"
              ),
            # Visa Fields
            "Visa_issue_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "Visa_expiry_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "Visa_status": forms.Select(attrs={"class": "form-control"}),
            "Visa_copy": forms.FileInput(attrs={"class": "form-control-file"}),
        }
# forms.py

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class CandidateSearchForm(forms.Form):
    query = forms.CharField(required=False, label="Search")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "GET"
        self.helper.add_input(Submit("search", "Search"))

