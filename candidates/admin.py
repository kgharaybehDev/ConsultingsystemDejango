# candidates/admin.py
from django.contrib import admin
from .models import (
    Candidate,
    Education,
    Experience,
    Language,
    TrainingCourse,
    CandidateApplicationData,
)


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "country", "created_at")
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("country", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("pk",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "degree", "field_of_study", "start_date", "end_date")
    search_fields = ("candidate__first_name", "candidate__last_name")
    list_filter = ("degree", "start_date")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("candidate", "company_name", "job_title", "start_date", "end_date")
    search_fields = ("candidate__first_name", "candidate__last_name", "company_name")
    list_filter = ("company_name", "start_date")


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("candidate", "language")
    search_fields = (
        "candidate__first_name",
        "candidate__last_name",
        "language__language",
    )


@admin.register(TrainingCourse)
class TrainingCourseAdmin(admin.ModelAdmin):
    list_display = ("candidate", "course_name", "institution", "start_date", "end_date")
    search_fields = ("candidate__first_name", "candidate__last_name", "course_name")
    list_filter = ("institution", "start_date")


@admin.register(CandidateApplicationData)
class CandidateApplicationDataAdmin(admin.ModelAdmin):
    list_display = ("candidate", "HMC_Portal_email", "JOB_OFFER_ID")
    search_fields = (
        "candidate__first_name",
        "candidate__last_name",
        "HMC_Portal_email",
    )
