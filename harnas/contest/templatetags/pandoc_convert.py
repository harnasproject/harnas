from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
import pypandoc
import bleach
from harnas.contest.bleach_whitelist import print_tags, print_attrs, all_styles


register = template.Library()


@register.filter
@stringfilter
def to_html(text):
    pandoc_args = [
        '--mathjax',
        '--smart',
    ]
    raw_html = pypandoc.convert(text,
                                'html',
                                format='md',
                                extra_args=pandoc_args)
    html = bleach.clean(raw_html,
                        print_tags,
                        print_attrs,
                        all_styles)
    html = raw_html
    return mark_safe(html)
