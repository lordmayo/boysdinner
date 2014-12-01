# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boysdinner', '0003_dish_current_dish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='served_date',
            field=models.DateField(auto_now=True, verbose_name=b'Date Dish Served'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dishvote',
            name='comment',
            field=models.CharField(max_length=400, null=True, blank=True),
            preserve_default=True,
        ),
    ]
