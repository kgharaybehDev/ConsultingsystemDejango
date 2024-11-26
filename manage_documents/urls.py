# manage_documents/urls.py

from django.urls import path

from . import views

app_name = "documents"
urlpatterns = [
    path(
        "candidate/<int:pk>/export_pdf/",
        views.candidate_export_pdf_CV,
        name="candidate_export_pdf_CV",
    ),
    # path(
    #     'candidate/<int:pk>/export_pdf_data_flow/',
    #     views.candidate_export_pdf_data_flow,
    #     name='candidate_export_pdf_data_flow',
    # ),
    #
    # HMC_Sheet URLs
    path(
        "hmc_sheet/<int:pk>/export_pdf/",
        views.HMC_Sheet,
        name="HMC_Sheet",
    ),
    # path(
    #     'hmc_sheet/<int:pk>/export_pdf_data_flow/',
    #     views.hmc_sheet_export_pdf_data_flow,
    #     name='hmc_sheet_export_pdf_data_flow',
    # ),
    # Job URLs
    # path(
    #     'job/<int:pk>/export_pdf/',
    #     views.job_export_pdf,
    #     name='job_export_pdf',
    # ),
    # path(
    #     'job/<int:pk>/export_pdf_data_flow/',
    #     views.job_export_pdf_data_flow,
]
