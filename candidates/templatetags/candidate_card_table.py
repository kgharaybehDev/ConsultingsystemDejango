from django import template
from django.shortcuts import get_object_or_404

from candidates.models import Candidate

register = template.Library()


@register.inclusion_tag("candidates/includes/candidate_card_table.html")
def candidate_card_table(candidate_id):
    candidate = get_object_or_404(Candidate, id=candidate_id)
    return {"candidate": candidate}
