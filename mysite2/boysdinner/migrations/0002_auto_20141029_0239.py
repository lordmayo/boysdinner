# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boysdinner', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dish',
            old_name='chef_name',
            new_name='chef',
        ),
    ]
