from django import template
from django.shortcuts import get_object_or_404

from candidates.models import Candidate

register = template.Library()


@register.inclusion_tag("candidates/includes/educations.html")
def educations(candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)

    _educations = candidate.educations.all().order_by("-start_date")
    return {"educations": _educations}
