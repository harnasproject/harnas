from hashlib import md5
from urllib.parse import urlencode


def gravatar_for_email(email, size=200):
    return "http://www.gravatar.com/avatar/%s?%s" % (
        md5(email.lower().encode()).hexdigest(),
        urlencode({'s': str(size)})
    )
