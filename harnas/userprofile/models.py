from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone


class UserProfile(models.Model):
    ORGANIZATION_CHOICES = (
        ('U', 'University'),
        ('J', 'Jagiellonian University'),
        ('S', 'High school'),
        ('H', 'Hobbyist')
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


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)
