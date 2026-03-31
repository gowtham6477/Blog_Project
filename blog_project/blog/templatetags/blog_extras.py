import re

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, phrase):
    if not text or not phrase:
        return text
    pattern = re.compile(re.escape(phrase), re.IGNORECASE)
    return mark_safe(pattern.sub(r"<mark>\g<0></mark>", text))
