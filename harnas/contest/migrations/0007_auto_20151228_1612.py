# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0006_auto_20151223_1805'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'permissions': (('view', 'Can view'), ('participate', 'Can participate'), ('manage', 'Can manage contest'))},
        ),
    ]
