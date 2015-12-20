# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='contest_id',
            field=models.ForeignKey(to='contest.Contest', default=0),
            preserve_default=False,
        ),
    ]
