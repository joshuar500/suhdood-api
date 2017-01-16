# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 06:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suhdood', '0003_auto_20170116_0544'),
    ]

    operations = [
        migrations.AddField(
            model_name='share',
            name='viewed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='url',
            name='url_string',
            field=models.URLField(max_length=500),
        ),
    ]
