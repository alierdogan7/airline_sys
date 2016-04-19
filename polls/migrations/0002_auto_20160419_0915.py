# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-19 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('airport_code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('airport_name', models.CharField(max_length=100)),
                ('supports_flight_legs', models.BooleanField(default=False)),
                ('max_airplanes', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_name', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('no_of_airports', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='airport',
            name='city_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.City'),
        ),
    ]
