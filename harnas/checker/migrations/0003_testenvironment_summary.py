# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0002_auto_20160102_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='testenvironment',
            name='summary',
            field=models.CharField(max_length=250, default=''),
            preserve_default=False,
        ),
    ]
