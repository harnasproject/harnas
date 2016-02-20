# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization', models.CharField(choices=[('U', 'University'), ('J', 'Jagiellonian University'), ('S', 'High school'), ('H', 'Hobbyist')], max_length=1, default='H')),
                ('date_of_birth', models.DateField(default=django.utils.timezone.now)),
                ('personal_page', models.URLField(blank=True, null=True)),
                ('show_email', models.BooleanField(default=False)),
                ('show_age', models.BooleanField(default=True)),
            ],
        ),
    ]
