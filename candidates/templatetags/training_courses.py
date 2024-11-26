from django import template
from django.shortcuts import get_object_or_404

from candidates.models import Candidate

register = template.Library()


@register.inclusion_tag("candidates/includes/trainingcourse_list.html")
def training_courses(candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    _training_courses = candidate.training_courses.all().order_by("-start_date")

    return {"training_courses": _training_courses}
