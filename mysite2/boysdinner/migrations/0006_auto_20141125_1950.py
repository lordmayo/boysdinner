# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boysdinner', '0005_auto_20141111_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='served_date',
            field=models.DateField(verbose_name=b'Date Dish Served'),
            preserve_default=True,
        ),
    ]
