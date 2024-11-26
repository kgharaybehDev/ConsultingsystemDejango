from django import template
from django.shortcuts import get_object_or_404

from candidates.models import Candidate

register = template.Library()


@register.inclusion_tag("candidates/includes/experiences.html")
def experiences(candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    _experiences = candidate.experiences.all().order_by("-start_date")
    return {"experiences": _experiences}
