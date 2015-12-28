from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import pypandoc
import bleach


register = template.Library()


@register.filter
@stringfilter
def to_html(text):
    pandoc_args = [
        '--mathjax',
        '--smart',
    ]
    raw_html = pypandoc.convert(text, 'html', format='md', extra_args=pandoc_args)
    # html = bleach.clean(raw_html)
    html = raw_html
    return mark_safe(html)
