# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boysdinner', '0004_auto_20141107_1255'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dishvote',
            unique_together=set([('critic', 'dish')]),
        ),
    ]
