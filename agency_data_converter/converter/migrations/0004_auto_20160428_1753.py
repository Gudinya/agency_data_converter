# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 14:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0003_auto_20160427_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flat',
            name='uid',
            field=models.CharField(max_length=255, verbose_name='Уникальный идентификатор'),
        ),
        migrations.AlterUniqueTogether(
            name='flat',
            unique_together=set([('uid', 'gilkvar')]),
        ),
    ]
