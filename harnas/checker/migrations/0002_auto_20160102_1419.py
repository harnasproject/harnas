# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('checker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testenvironment',
            name='template_id',
        ),
        migrations.AddField(
            model_name='testenvironment',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testenvironment',
            name='maintainer',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testenvironment',
            name='template_name',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
