from hashlib import md5
from urllib.parse import urlencode
from django.contrib.sites.models import Site

from harnas import settings


def gravatar_for_user(user, size=200):
    default = 'default_gravatar_male' if user.userprofile.sex == 'M' \
        else 'default_gravatar_female'

    return "http://www.gravatar.com/avatar/%s?%s" % (
        md5(user.email.lower().encode()).hexdigest(),
        urlencode({
            's': str(size),
            'd': 'http://%s%s%s' %
            # EXPERIMENTAL !!! need to be tested in production
                 (Site.objects.get_current(), settings.STATIC_URL, default)
        })
    )
