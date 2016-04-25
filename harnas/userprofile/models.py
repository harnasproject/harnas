from datetime import date
from hashlib import md5
from urllib.parse import urlencode

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone
from harnas import settings


class UserProfile(models.Model):
    """
    Model used to extend user account informations.
    """
    ORGANIZATION_CHOICES = (
        ('U', 'University'),
        ('J', 'Jagiellonian University'),
        ('S', 'High school'),
        ('H', 'Hobbyist')
    )

    SEX_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    user = models.OneToOneField(
          User,
          primary_key=True
    )
    organization = models.CharField(
          max_length=1,
          choices=ORGANIZATION_CHOICES,
          default='H'
    )
    date_of_birth = models.DateField(
          default=timezone.now
    )
    sex = models.CharField(
        max_length=1,
        default='M',
        choices=SEX_CHOICES
    )
    personal_page = models.URLField(
          null=True,
          blank=True
    )
    show_email = models.BooleanField(
          default=False
    )
    show_age = models.BooleanField(
          default=True
    )

    @property
    def display_name(self):
        if (self.user.first_name is not None and self.user.first_name.strip() != "") or \
                (self.user.last_name is not None and self.user.last_name.strip() != ""):
            return self.user.first_name + " " + self.user.last_name
        else:
            return self.user.username

    @property
    def gravatar(self, size=200):
        default = 'default_gravatar_male' if self.sex == 'M' \
            else 'default_gravatar_female'

        return "http://www.gravatar.com/avatar/%s?%s" % (
            md5(self.user.email.lower().encode()).hexdigest(),
            urlencode({
                's': str(size),
                'd': 'http://%s%s%s' %
                # EXPERIMENTAL !!! need to be tested in production
                     (Site.objects.get_current(), settings.STATIC_URL, default)
            })
        )

    @property
    def age(self):
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - (
            (today.month, today.day) < (born.month, born.day))


def create_user_profile(sender, instance, created, **kwargs):
    """
    Function used to create user profile instance right after new user is
    created.
    """
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
