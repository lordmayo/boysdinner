# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boysdinner', '0002_auto_20141029_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='current_dish',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
