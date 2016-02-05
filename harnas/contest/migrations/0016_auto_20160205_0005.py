# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0015_auto_20160204_2323'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contest',
            options={'permissions': (('view_contest', 'Can view'), ('participate_in_contest', 'Can participate'), ('manage_contest', 'Can manage contest'))},
        ),
    ]
