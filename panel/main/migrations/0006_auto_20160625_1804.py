# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-25 18:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20160625_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='roi',
            options={'verbose_name': 'Rectangle of Interest', 'verbose_name_plural': 'Rectangles of Interest'},
        ),
    ]