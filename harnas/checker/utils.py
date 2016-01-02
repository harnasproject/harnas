from django.conf import settings
from django.core.cache import cache
from harnas.checker.heraclient import Template


def get_templates_list():
    # Hera does not currently show public templates so we need to hardcode
    # templates = Template.list(settings.HERA_AUTH)
    templates = cache.get('templates_list')
    if templates is None:
        templates = [ Template('debian-jessie', settings.HERA_AUTH) ]
        cache.set('templates_list', templates, 60 * 60 * 24)
    return templates
