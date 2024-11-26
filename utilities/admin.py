# candidates/admin.py

from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Country,
    Nationality,
    DegreeChoices,
    FieldOfStudy,
    Institution,
    EducationGradeChoices,
    LanguageChoices,
    Department,
    LicenseProvider,
)


@admin.register(Country)
class CountryAdmin(SimpleHistoryAdmin):
    list_display = ("code", "name")
    search_fields = ("code", "name")
    ordering = ("name",)


@admin.register(Nationality)
class NationalityAdmin(SimpleHistoryAdmin):
    list_display = ("nationality_name",)
    search_fields = ("nationality_name",)
    ordering = ("nationality_name",)


@admin.register(DegreeChoices)
class DegreeChoicesAdmin(SimpleHistoryAdmin):
    list_display = ("degree",)
    search_fields = ("degree",)
    ordering = ("degree",)


@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(SimpleHistoryAdmin):
    list_display = ("field_of_study",)
    search_fields = ("field_of_study",)
    ordering = ("field_of_study",)


@admin.register(Institution)
class InstitutionAdmin(SimpleHistoryAdmin):
    list_display = ("abbreviation", "type", "institution", "country")
    search_fields = ("abbreviation", "institution", "country__name")
    list_filter = ("type", "country")
    ordering = ("type", "institution")


@admin.register(EducationGradeChoices)
class EducationGradeChoicesAdmin(SimpleHistoryAdmin):
    list_display = ("grade",)
    search_fields = ("grade",)
    ordering = ("grade",)


@admin.register(LanguageChoices)
class LanguageChoicesAdmin(SimpleHistoryAdmin):
    list_display = ("language",)
    search_fields = ("language",)
    ordering = ("language",)


@admin.register(Department)
class DepartmentAdmin(SimpleHistoryAdmin):
    list_display = ("abbreviation", "title")
    search_fields = ("abbreviation", "title")
    ordering = ("title",)


@admin.register(LicenseProvider)
class DepartmentAdmin(SimpleHistoryAdmin):
    list_display = ("name", "country")
    search_fields = ("country", "name")
    ordering = ("name",)
