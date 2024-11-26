from django import template
from django.shortcuts import get_object_or_404

from candidates.models import Candidate

register = template.Library()


@register.inclusion_tag("candidates/includes/languages.html")
def languages(candidate_pk):
    candidate = get_object_or_404(Candidate, pk=candidate_pk)
    _languages = candidate.languages.all()
    return {"languages": _languages}
