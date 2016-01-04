from django.conf import settings
from django.core.cache import cache
from harnas.checker.heraclient import Template


def get_templates_list():
    templates = cache.get('templates_list')
    if templates is None:
        templates = Template.list(settings.HERA_AUTH)
        cache.set('templates_list', templates, 60 * 60 * 24)
    return templates
