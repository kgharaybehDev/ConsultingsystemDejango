# candidates/urls.py
from django.urls import path
from . import views


app_name = "candidates"

urlpatterns = [
    # Candidate URLs

    path("search/", views.candidate_search_view, name="candidate_search"),

    path("", views.candidate_list, name="candidate_list"),
    path("create/", views.candidate_create, name="candidate_create"),
    path("<int:pk>/", views.candidate_detail, name="candidate_detail"),
    path("<int:pk>/update/", views.candidate_update, name="candidate_update"),
    path("<int:pk>/delete/", views.candidate_delete, name="candidate_delete"),
    # File Deletion URLs
    path(
        "<int:candidate_pk>/delete_resume/", views.delete_resume, name="delete_resume"
    ),
    path(
        "<int:candidate_pk>/delete_personal_image/",
        views.delete_personal_image,
        name="delete_personal_image",
    ),
    path(
        "<int:candidate_pk>/delete_id_copy/",
        views.delete_id_copy,
        name="delete_id_copy",
    ),
    path(
        "<int:candidate_pk>/delete_passport_copy/",
        views.delete_passport_copy,
        name="delete_passport_copy",
    ),
    # Education URLs
    path(
        "<int:candidate_pk>/educations/create/",
        views.education_create,
        name="education_create",
    ),
    path(
        "educations/<int:pk>/update/", views.education_update, name="education_update"
    ),
    path(
        "educations/<int:pk>/delete/", views.education_delete, name="education_delete"
    ),
    # Education File Deletion
    path(
        "educations/<int:education_pk>/delete_certification/",
        views.delete_education_certification,
        name="delete_education_certification",
    ),
    path(
        "educations/<int:education_pk>/delete_transcript/",
        views.delete_education_transcript,
        name="delete_education_transcript",
    ),
    # Experience URLs
    path(
        "<int:candidate_pk>/experiences/create/",
        views.experience_create,
        name="experience_create",
    ),
    path(
        "experiences/<int:pk>/update/",
        views.experience_update,
        name="experience_update",
    ),
    path(
        "experiences/<int:pk>/delete/",
        views.experience_delete,
        name="experience_delete",
    ),
    # Experience File Deletion
    path(
        "experiences/<int:experience_pk>/delete_certification/",
        views.delete_experience_certification,
        name="delete_experience_certification",
    ),
    # Language URLs
    path(
        "languages/<int:candidate_pk>/languages/create/",
        views.language_create,
        name="language_create",
    ),
    path("languages/<int:pk>/delete/", views.language_delete, name="language_delete"),
    # Training Course URLs
    path(
        "<int:candidate_pk>/training_courses/create/",
        views.training_course_create,
        name="training_course_create",
    ),
    path(
        "training_courses/<int:pk>/update/",
        views.training_course_update,
        name="training_course_update",
    ),
    path(
        "training_courses/<int:pk>/delete/",
        views.training_course_delete,
        name="training_course_delete",
    ),
    # Training Course File Deletion
    path(
        "<int:training_course_pk>/delete_certification/",
        views.delete_training_course_certification,
        name="delete_training_course_certification",
    ),
    # License URLs
    path(
        "<int:candidate_pk>/licenses/create/",
        views.license_create,
        name="license_create",
    ),
    path("licenses/<int:pk>/update/", views.license_update, name="license_update"),
    path("licenses/<int:pk>/delete/", views.license_delete, name="license_delete"),
    # License File Deletion
    path(
        "<int:license_pk>/delete_license_copy/",
        views.delete_license_copy,
        name="delete_license_copy",
    ),
    # Candidate Application Data URLs
    path(
        "<int:candidate_pk>/application_data/update/",
        views.candidate_application_data_update,
        name="candidate_application_data_update",
    ),
    path(
        "<int:candidate_pk>/application_data/detail/",
        views.candidate_application_data_detail,
        name="candidate_application_data_detail",
    ),
    path(
        "candidate/<int:candidate_id>/delete_blood_test_report/",
        views.delete_blood_test_report,
        name="delete_blood_test_report",
    ),
    path(
        "candidate/<int:candidate_id>/delete_xray_test_report/",
        views.delete_xray_test_report,
        name="delete_xray_test_report",
    ),
    path(
        "candidate/<int:candidate_id>/delete_fit_to_work_report/",
        views.delete_fit_to_work_report,
        name="delete_fit_to_work_report",
    ),
    # DataFlow_certificate_copy
    path(
        "candidate/<int:candidate_id>/delete_dataflow_certificate/",
        views.delete_dataflow_certificate,
        name="delete_dataflow_certificate_copy",
    ),
    path(
        "candidate/<int:candidate_id>/delete_pregnancy_report/",
        views.delete_pregnancy_report,
        name="delete_pregnancy_report",
    ),
    path(
        "candidate/<int:candidate_id>/delete_dhp_certificate/",
        views.delete_dhp_certificate,
        name="delete_dhp_certificate",
    ),
    path(
        "candidate/<int:candidate_id>/delete_prometric_certificate/",
        views.delete_prometric_certificate,
        name="delete_prometric_certificate",
    ),
# delete_prometric_appointment
    path(
        "candidate/<int:candidate_id>/delete_prometric_appointment_copy/",
        views.delete_prometric_appointment_copy,
        name="delete_prometric_appointment_copy",
    ),
    # delete_police_clearance_copy
    path(
        "candidate/<int:candidate_id>/delete_police_clearance_copy/",
        views.delete_police_clearance_copy,
        name="delete_police_clearance_copy",
    ),
    # delete_visa_copy
    path(
        "candidate/<int:candidate_id>/delete_visa_copy/",
        views.delete_visa_copy,
        name="delete_visa_copy",
    ),
    path(

        "candidate/<int:candidate_id>/delete_police_clearance_copy/",
        views.delete_police_clearance_copy,
        name="delete_police_clearance_copy",
    ),
    path(
        "candidate/<int:candidate_id>/delete_visa_copy/",
        views.delete_visa_copy,
        name="delete_visa_copy",
    ),

    path('download/', views.download_file, name='download_file'),

    path('download-directory/<int:candidate_id>/', views.download_candidate_directory,
         name='download_candidate_directory'),
    path('download-vcf/<int:candidate_id>/', views.download_vcf, name='download_vcf'),

]
