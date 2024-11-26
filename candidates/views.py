# candidates/views.py
import re
from urllib.parse import quote

import unicodedata
import vobject
from django.contrib import messages
from django.contrib.postgres.search import SearchVector
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from .forms import (
    CandidateForm,
    EducationForm,
    ExperienceForm,
    LanguageForm,
    TrainingCourseForm,
    CandidateApplicationDataForm,
    LicenseForm, )
from .forms import CandidateSearchForm
from .models import (
    Education,
    Experience,
    Language,
    TrainingCourse,
    CandidateApplicationData,
    License,
)


def candidate_list(request):
    # Sorting logic
    sort_by = request.GET.get("sort", "created_at")  # Default sorting by created_at
    order = request.GET.get("order", "desc")  # Default order is descending
    order_prefix = "-" if order == "desc" else ""

    # Map "full_name" to "first_name" and add secondary sorting for other name fields
    if sort_by == "full_name":
        sort_criteria = [f"{order_prefix}first_name", f"{order_prefix}second_name", f"{order_prefix}last_name"]
    else:
        sort_criteria = [f"{order_prefix}{sort_by}"]

    # Query and sort candidates
    candidates = Candidate.objects.all().order_by(*sort_criteria)

    # Items per page logic
    per_page = request.GET.get("per_page", 10)  # Default is 10 items per page
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10  # Fallback to default if invalid input

    paginator = Paginator(candidates, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Column names and their display labels
    columns = [
        {"name": "full_name", "label": "Full Name"},
        {"name": "email", "label": "Email"},
        {"name": "nationality", "label": "Nationality"},
        {"name": "total_experience", "label": "Total Experience"},
        {"name": "departments", "label": "Departments"},
        {"name": "updated_at", "label": "Last Updated"},
    ]

    context = {
        "candidates": page_obj,
        "sort_by": sort_by,
        "order": order,
        "per_page": per_page,
        "columns": columns,
    }
    return render(request, "candidates/candidate_list.html", context)




def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)

    context = {"candidate": candidate}
    return render(request, "candidates/candidate_detail.html", context)


def candidate_create(request):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, "Candidate created successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = CandidateForm()
    return render(request, "candidates/candidate_form.html", {"form": form})


def candidate_update(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Candidate updated successfully.")
                return redirect("candidates:candidate_detail", pk=candidate.pk)
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = CandidateForm(instance=candidate)
    return render(
        request,
        "candidates/candidate_form.html",
        {"form": form, "candidate": candidate},
    )


def candidate_delete(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.method == "POST":
        candidate.delete()
        messages.success(request, "Candidate deleted successfully.")
        return redirect("candidates:candidate_list")
    return render(request, "candidates/candidate_delete.html", {"candidate": candidate})


# Education Views
def education_create(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "POST":
        form = EducationForm(request.POST, request.FILES)
        if form.is_valid():
            education = form.save(commit=False)
            education.candidate = candidate
            # Save the education object to get a primary key
            education.save()
            # Attach the file and save again
            form.save_m2m()
            messages.success(request, "Education added successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = EducationForm()
    return render(
        request,
        "candidates/education_form.html",
        {"form": form, "candidate": candidate},
    )


def education_update(request, pk):
    education = get_object_or_404(Education, pk=pk)
    candidate = education.candidate
    if request.method == "POST":
        form = EducationForm(request.POST, request.FILES, instance=education)
        if form.is_valid():
            form.save()
            messages.success(request, "Education updated successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = EducationForm(instance=education)
    return render(
        request,
        "candidates/education_form.html",
        {"form": form, "candidate": candidate},
    )


def education_delete(request, pk):
    education = get_object_or_404(Education, pk=pk)
    candidate = education.candidate
    if request.method == "POST":
        education.delete()
        messages.success(request, "Education deleted successfully.")
        return redirect("candidates:candidate_detail", pk=candidate.pk)
    return render(
        request,
        "candidates/education_delete.html",
        {"education": education, "candidate": candidate},
    )


# Experience Views
def experience_create(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "POST":
        form = ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.candidate = candidate
            experience.save()
            form.save_m2m()
            messages.success(request, "Experience added successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = ExperienceForm()
    return render(
        request,
        "candidates/experience_form.html",
        {"form": form, "candidate": candidate},
    )


def experience_update(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    candidate = experience.candidate
    if request.method == "POST":
        form = ExperienceForm(request.POST, request.FILES, instance=experience)
        if form.is_valid():
            form.save()
            messages.success(request, "Experience updated successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = ExperienceForm(instance=experience)
    return render(
        request,
        "candidates/experience_form.html",
        {"form": form, "candidate": candidate},
    )


def experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    candidate = experience.candidate
    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted successfully.")
        return redirect("candidates:candidate_detail", pk=candidate.pk)
    return render(
        request,
        "candidates/experience_delete.html",
        {"experience": experience, "candidate": candidate},
    )


# Language Views
def language_create(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "POST":
        form = LanguageForm(request.POST)
        if form.is_valid():
            language = form.save(commit=False)
            language.candidate = candidate
            language.save()
            messages.success(request, "Language added successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = LanguageForm()
    return render(
        request, "candidates/language_form.html", {"form": form, "candidate": candidate}
    )


def language_delete(request, pk):
    language = get_object_or_404(Language, pk=pk)
    candidate = language.candidate
    if request.method == "POST":
        language.delete()
        messages.success(request, "Language deleted successfully.")
        return redirect("candidates:candidate_detail", pk=candidate.pk)
    return render(
        request,
        "candidates/language_delete.html",
        {"language": language, "candidate": candidate},
    )


# Training Course Views
def training_course_create(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "POST":
        form = TrainingCourseForm(request.POST, request.FILES)
        if form.is_valid():
            training_course = form.save(commit=False)
            training_course.candidate = candidate
            training_course.save()
            messages.success(request, "Training course added successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = TrainingCourseForm()
    return render(
        request,
        "candidates/trainingcourse_form.html",
        {"form": form, "candidate": candidate},
    )


def training_course_update(request, pk):
    training_course = get_object_or_404(TrainingCourse, pk=pk)
    candidate = training_course.candidate
    if request.method == "POST":
        form = TrainingCourseForm(request.POST, request.FILES, instance=training_course)
        if form.is_valid():
            form.save()
            messages.success(request, "Training course updated successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = TrainingCourseForm(instance=training_course)
    return render(
        request,
        "candidates/trainingcourse_form.html",
        {"form": form, "candidate": candidate},
    )


def training_course_delete(request, pk):
    training_course = get_object_or_404(TrainingCourse, pk=pk)
    candidate = training_course.candidate
    if request.method == "POST":
        training_course.delete()
        messages.success(request, "Training course deleted successfully.")
        return redirect("candidates:candidate_detail", pk=candidate.pk)
    return render(
        request,
        "candidates/trainingcourse_delete.html",
        {"training_course": training_course, "candidate": candidate},
    )


# Candidate Application Data Views
def candidate_application_data_update(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    try:
        application_data = candidate.application_data
    except CandidateApplicationData.DoesNotExist:
        application_data = CandidateApplicationData(
            candidate=candidate,
            HMC_Portal_email=candidate.email,
            HMC_Portal_password=candidate.first_name[0].upper() + "@1592",
            DataFlow_passport_number=candidate.passport_id,
            DHP_email=candidate.email,
            DHP_Password=candidate.first_name[0].upper() + "@1592",
        )

    if request.method == "POST":
        form = CandidateApplicationDataForm(
            request.POST, request.FILES, instance=application_data
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Application data updated successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = CandidateApplicationDataForm(instance=application_data)
    return render(
        request,
        "candidates/candidate_application_data_form.html",
        {"form": form, "candidate": candidate},
    )


def candidate_application_data_detail(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    try:
        application_data = candidate.application_data
    except CandidateApplicationData.DoesNotExist:
        application_data = None
    return render(
        request,
        "candidates/candidate_application_data_detail.html",
        {"application_data": application_data, "candidate": candidate},
    )


def license_create(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "POST":
        form = LicenseForm(request.POST, request.FILES)
        if form.is_valid():
            license = form.save(commit=False)
            license.candidate = candidate
            license.save()
            messages.success(request, "License added successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = LicenseForm()
    return render(
        request,
        "candidates/license_form.html",
        {"form": form, "candidate": candidate},
    )


def license_update(request, pk):
    _license = get_object_or_404(License, pk=pk)
    candidate = _license.candidate
    if request.method == "POST":
        form = LicenseForm(request.POST, request.FILES, instance=_license)
        if form.is_valid():
            form.save()
            messages.success(request, "License updated successfully.")
            return redirect("candidates:candidate_detail", pk=candidate.pk)
    else:
        form = LicenseForm(instance=_license)
    return render(
        request,
        "candidates/license_form.html",
        {"form": form, "candidate": candidate},
    )


def license_delete(request, pk):
    license = get_object_or_404(License, pk=pk)
    candidate = license.candidate
    if request.method == "POST":
        license.delete()
        messages.success(request, "License deleted successfully.")
        return redirect("candidates:candidate_detail", pk=candidate.pk)
    return render(
        request,
        "candidates/license_delete.html",
        {"license": license, "candidate": candidate},
    )


# DELETE FILE VIEW


# View to delete resume
def delete_resume(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "GET":
        try:
            candidate.delete_resume()
            messages.success(request, "Resume deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting resume: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete personal image
def delete_personal_image(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "GET":
        try:
            candidate.delete_image()
            messages.success(request, "Personal image deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting personal image: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete national ID copy
def delete_id_copy(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "GET":
        try:
            candidate.delete_id_copy()
            messages.success(request, "National ID copy deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting national ID copy: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete passport copy
def delete_passport_copy(request, candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    if request.method == "GET":
        try:
            candidate.delete_passport_copy()
            messages.success(request, "Passport copy deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting passport copy: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete education certification
def delete_education_certification(request, education_pk):
    education = get_object_or_404(Education, pk=education_pk)
    candidate = education.candidate
    if request.method == "GET":
        try:
            education.delete_certification_copy()
            messages.success(request, "Education certification deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting education certification: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete education transcript
def delete_education_transcript(request, education_pk):
    education = get_object_or_404(Education, pk=education_pk)
    candidate = education.candidate
    if request.method == "GET":
        try:
            education.delete_transcript_copy()
            messages.success(request, "Education certification deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting education certification: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete experience certification
def delete_experience_certification(request, experience_pk):
    experience = get_object_or_404(Experience, pk=experience_pk)
    candidate = experience.candidate
    if request.method == "GET":
        try:
            experience.delete_certification_copy()
            messages.success(request, "Experience certification deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting experience certification: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete training course certification
def delete_training_course_certification(request, training_course_pk):
    training_course = get_object_or_404(TrainingCourse, pk=training_course_pk)
    candidate = training_course.candidate
    if request.method == "GET":
        try:
            training_course.delete_certification_copy()
            messages.success(
                request, "Training course certification deleted successfully."
            )
        except Exception as e:
            messages.error(
                request, f"Error deleting training course certification: {e}"
            )
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete license copy
def delete_license_copy(request, license_pk):
    _license = get_object_or_404(License, pk=license_pk)
    candidate = _license.candidate
    if request.method == "GET":
        try:
            _license.delete_license_copy()
            messages.success(request, "License copy deleted successfully.")
        except Exception as e:
            messages.error(request, f"Error deleting license copy: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete Blood Test Report
def delete_blood_test_report(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_blood_test_report()
        messages.success(request, "Blood Test Report deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Blood Test Report: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete X-Ray Test Report
def delete_xray_test_report(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_xray_test_report()
        messages.success(request, "X-Ray Test Report deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting X-Ray Test Report: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete Fit to Work Report
def delete_fit_to_work_report(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_fit_to_work_report()
        messages.success(request, "Fit to Work Report deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Fit to Work Report: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# delete_dataflow_certificate
def delete_dataflow_certificate(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_dataflow_certificate_copy()
        messages.success(request, "Dataflow Certificate deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Dataflow Certificate: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete Pregnancy Report
def delete_pregnancy_report(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_pregnancy_report()
        messages.success(request, "Pregnancy Report deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Pregnancy Report: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete DHP Certificate Copy
def delete_dhp_certificate(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_dhp_certificate()
        messages.success(request, "DHP Certificate deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting DHP Certificate: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete Prometric Certificate Copy
def delete_prometric_certificate(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_prometric_certificate()
        messages.success(request, "Prometric Certificate deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Prometric Certificate: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete Police Clearance Certificate Copy
def delete_police_clearance_copy(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_police_clearance_copy()
        messages.success(request, "Police Clearance Certificate deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Police Clearance Certificate: {e}")
    return redirect(request.META.get("HTTP_REFERER"))


# View to delete Visa Copy
def delete_visa_copy(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_visa_copy()
        messages.success(request, "Visa Copy deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Visa Copy: {e}")
    return redirect(request.META.get("HTTP_REFERER"))



# views.py





def candidate_search_view(request):
    form = CandidateSearchForm(request.GET or None)
    candidates = Candidate.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get("query")
        if query:
            candidates = Candidate.objects.annotate(
                search=SearchVector(
                    'first_name', 'second_name', 'third_name', 'last_name',
                    'national_id_number', 'passport_id',
                    'whatsapp_phone_number', 'call_phone_number', 'email'
                )
            ).filter(search=query)

    # Sorting logic
    sort_by = request.GET.get("sort", "first_name")  # Default sort field
    order = request.GET.get("order", "asc")  # Default order is ascending
    order_prefix = "" if order == "asc" else "-"
    candidates = candidates.order_by(f"{order_prefix}{sort_by}")

    # Pagination logic
    per_page = int(request.GET.get("per_page", 10))  # Default 10 items per page
    paginator = Paginator(candidates, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "form": form,
        "candidates": page_obj,
        "sort_by": sort_by,
        "order": order,
        "per_page": per_page,
    }
    return render(request, "candidates/search.html", context)


# baseapp/candidates/views.py
import urllib.parse

def download_file(request):
    """
    Download a file by its key from the S3 bucket and return as response.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    file_url = request.GET.get('file_key')

    if not file_url:
        return HttpResponse("File key not provided", status=400)

    try:
        # Decode URL-encoded file URL
        file_url = urllib.parse.unquote(file_url)

        # Extract key from the file URL
        file_key = file_url.replace(f"https://{bucket_name}.s3.amazonaws.com/", "")
        file_key = file_key.lstrip('/')

        # Get file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)

        # Return file as HTTP response
        file_data = response['Body'].read()
        content_type = response.get('ContentType', 'application/octet-stream')

        return HttpResponse(
            file_data,
            content_type=content_type,
            headers={
                'Content-Disposition': f'attachment; filename="{file_key.split("/")[-1]}"',
            }
        )
    except NoCredentialsError:
        return HttpResponse("AWS credentials not available", status=500)
    except PartialCredentialsError:
        return HttpResponse("Incomplete AWS credentials", status=500)
    except s3_client.exceptions.NoSuchKey:
        raise Http404("File not found")
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


# baseapp/candidates/views.py

import zipfile
from django.http import HttpResponse, Http404, StreamingHttpResponse
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.conf import settings
from .models import Candidate, get_candidate_directory
from django.contrib.auth.decorators import login_required
import zipstream  # For streaming large ZIP files

@login_required
def download_candidate_directory(request, candidate_id):
    """
    Download the candidate's directory from S3 as a ZIP file.
    """
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
    )
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME

    try:
        # Get the candidate instance
        candidate = Candidate.objects.get(pk=candidate_id)

        # Construct the candidate directory path
        candidate_directory = get_candidate_directory(candidate)

        # Ensure the directory path ends with '/'
        if not candidate_directory.endswith('/'):
            candidate_directory += '/'

        # List all objects in the candidate's directory
        paginator = s3_client.get_paginator('list_objects_v2')
        page_iterator = paginator.paginate(Bucket=bucket_name, Prefix=candidate_directory)

        # Initialize zipstream.ZipFile for streaming
        z = zipstream.ZipFile(mode='w', compression=zipfile.ZIP_DEFLATED)

        files_found = False
        for page in page_iterator:
            if 'Contents' in page:
                files_found = True
                for obj in page['Contents']:
                    file_key = obj['Key']

                    # Exclude directories
                    if file_key.endswith('/'):
                        continue

                    # Get the file content as a stream
                    file_obj = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                    file_stream = file_obj['Body']

                    # Use relative paths inside the ZIP file
                    relative_path = file_key[len(candidate_directory):]

                    # Add the file to the ZIP archive
                    z.write_iter(relative_path, file_stream)

        if not files_found:
            return HttpResponse("No files found in the candidate's directory.", status=404)

        # Stream the ZIP file as HTTP response
        response = StreamingHttpResponse(z, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{candidate.full_name}_files.zip"'

        return response

    except Candidate.DoesNotExist:
        raise Http404("Candidate not found.")
    except NoCredentialsError:
        return HttpResponse("AWS credentials not available.", status=500)
    except PartialCredentialsError:
        return HttpResponse("Incomplete AWS credentials.", status=500)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


# baseapp/candidates/views.py (continued)
def slugify_filename(filename):
    """
    Generate a safe ASCII filename by normalizing Unicode characters and removing unsafe characters.
    """
    # Normalize the unicode characters to ASCII equivalents
    normalized = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('ascii')
    # Remove any characters that are not alphanumeric, spaces, dots, underscores, or hyphens
    safe_filename = re.sub(r'[^\w\s.-]', '', normalized).strip()
    # Replace spaces with underscores
    safe_filename = re.sub(r'[-\s]+', '_', safe_filename)
    return safe_filename

def download_vcf(request, candidate_id):
    """
    Generate and download a VCF file for a candidate.
    """
    try:
        # Get the candidate instance
        candidate = Candidate.objects.get(pk=candidate_id)

        # Generate VCF content
        vcf_content = generate_candidate_vcf(candidate)

        # Create HTTP response with VCF content
        response = HttpResponse(vcf_content, content_type='text/vcard; charset=utf-8')

        # Original filename with special characters
        filename = f"{candidate.full_name}.vcf"

        # Generate a safe ASCII filename
        ascii_filename = slugify_filename(filename)

        # URL-encode the UTF-8 filename
        utf8_filename = quote(filename)

        # Set the Content-Disposition header with both filename and filename*
        response['Content-Disposition'] = f"attachment; filename=\"{ascii_filename}\"; filename*=UTF-8''{utf8_filename}"

        return response

    except Candidate.DoesNotExist:
        raise Http404("Candidate not found.")
def generate_candidate_vcf(candidate):
    """
    Generate VCF formatted string for a candidate using vobject library.
    """
    vcard = vobject.vCard()

    # Name
    vcard.add('n')
    vcard.n.value = vobject.vcard.Name(
        family=candidate.last_name or '',
        given=candidate.first_name or '',
        additional=' '.join(filter(None, [candidate.second_name, candidate.third_name])) or ''
    )
    vcard.add('fn')
    vcard.fn.value = candidate.full_name

    # Email
    if candidate.email:
        email = vcard.add('email')
        email.value = candidate.email
        email.type_param = 'INTERNET'

    # Cell Phone
    if candidate.call_phone_number:
        tel = vcard.add('tel')
        tel.value = candidate.call_phone_number
        tel.type_param = 'CELL'

    # WhatsApp Phone
    if candidate.whatsapp_phone_number:
        tel = vcard.add('tel')
        tel.value = candidate.whatsapp_phone_number
        tel.type_param = 'VOICE'

    # Address
    if candidate.address or candidate.country:
        adr = vcard.add('adr')
        adr.value = vobject.vcard.Address(
            street=candidate.address or '',
            city='',
            region='',
            code='',
            country=candidate.country.name if candidate.country else ''
        )
        adr.type_param = 'HOME'

    # Birthday
    if candidate.birthday:
        bday = vcard.add('bday')
        bday.value = candidate.birthday.strftime('%Y-%m-%d')

    # Notes (Optional)
    # You can add more fields as needed, such as notes or URLs.

    # Serialize to string
    vcf_content = vcard.serialize()

    return vcf_content


def delete_prometric_appointment_copy(request, candidate_id):
    candidate_data = get_object_or_404(
        CandidateApplicationData, candidate_id=candidate_id
    )
    try:
        candidate_data.delete_prometric_appointment_copy()
        messages.success(request, "Prometric Appointment Copy deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting Prometric Appointment Copy: {e}")
    return redirect(request.META.get("HTTP_REFERER"))
