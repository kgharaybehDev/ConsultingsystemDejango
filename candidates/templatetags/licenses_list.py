from django import template
from django.shortcuts import get_object_or_404

from candidates.models import Candidate

register = template.Library()


@register.inclusion_tag("candidates/includes/licenses.html")
def licenses(candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    _licenses = candidate.licenses.all().order_by("-issued_date")
    return {"licenses": _licenses}
