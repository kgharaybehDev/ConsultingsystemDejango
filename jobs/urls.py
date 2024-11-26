from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.job_opportunity_list, name='job_opportunity_list'),
    path('job-opportunities/', views.job_opportunity_list, name='job_opportunity_list'),
    path('job-opportunities/add/', views.job_opportunity_create, name='job_opportunity_create'),
    path('job-opportunities/<int:pk>/', views.job_opportunity_detail, name='job_opportunity_detail'),
    path('job-opportunities/<int:pk>/edit/', views.job_opportunity_edit, name='job_opportunity_edit'),
    path('job-opportunities/<int:pk>/candidates/', views.job_opportunity_candidates, name='job_opportunity_candidates'),
    # This endpoint is not used in the provided code. If you want to include it, you can uncomment it and modify the view function accordingly.
    path('job-opportunities/<int:pk>/compatible-candidates/', views.job_opportunity_compatible_candidates, name='job_opportunity_compatible_candidates'),
    path('job-opportunities/<int:job_id>/add-candidate/<int:candidate_id>/', views.job_opportunity_add_candidate, name='job_opportunity_add_candidate'),
    path('job-opportunities/<int:job_id>/remove-candidate/<int:candidate_id>/', views.job_opportunity_remove_candidate, name='job_opportunity_remove_candidate'),
]
