from django import template

register = template.Library()


@register.inclusion_tag("includes/document_preview.html")
def document_preview(document_url_temp=None):
    document_url = document_url_temp
    return {"document_url": document_url}
