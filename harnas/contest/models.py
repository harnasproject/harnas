from django.db import models

class Contest(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField()

    class Meta:
        permissions = (
            ('view', 'Can view'),
            ('participant', 'Can participate'),
            ('manager', 'Can manage contest'))
