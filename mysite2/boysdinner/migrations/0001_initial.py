# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dish_name', models.CharField(max_length=200)),
                ('served_date', models.DateTimeField(verbose_name=b'Date Dish Served')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DishVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('taste_rating', models.IntegerField(default=0)),
                ('originality_rating', models.IntegerField(default=0)),
                ('presentation_rating', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=400, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='dishvote',
            name='critic',
            field=models.ForeignKey(to='boysdinner.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dishvote',
            name='dish',
            field=models.ForeignKey(to='boysdinner.Dish'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dish',
            name='chef_name',
            field=models.ForeignKey(to='boysdinner.Person'),
            preserve_default=True,
        ),
    ]
