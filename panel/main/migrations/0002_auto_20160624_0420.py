# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 04:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
