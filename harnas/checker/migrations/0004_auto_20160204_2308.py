# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0003_testenvironment_summary'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testenvironment',
            options={'permissions': 'view_test_'},
        ),
    ]
