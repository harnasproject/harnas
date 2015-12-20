# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0004_auto_20151220_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcase',
            name='max_duration',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testcase',
            name='max_memory',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='testenvironment',
            name='template_name',
            field=models.CharField(max_length=250, default=''),
            preserve_default=False,
        ),
    ]
