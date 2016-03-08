# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checker', '0005_auto_20160204_2309'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testenvironment',
            options={'permissions': (('view_test_environment', 'Can view test environment'), ('edit_test_environment', 'Can edit test environment'))},
        ),
    ]
