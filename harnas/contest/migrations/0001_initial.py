# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField()),
            ],
            options={
                'permissions': (('view', 'Can view'), ('participant', 'Can participate'), ('manager', 'Can manage contest')),
            },
        ),
    ]
