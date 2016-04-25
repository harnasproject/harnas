# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0007_submit'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='webhook_secret',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
