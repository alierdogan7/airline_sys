# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-20 06:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20160420_0621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seat',
            name='seat_class',
            field=models.CharField(choices=[('business', 'Business Class'), ('economy', 'Economy Class')], max_length=20),
        ),
    ]
