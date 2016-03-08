# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0017_auto_20160305_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskedition',
            name='contest',
            field=models.ForeignKey(to='contest.Contest', default=''),
            preserve_default=False,
        ),
    ]
