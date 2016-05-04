# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_reservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('flight_id', models.AutoField(primary_key=True, serialize=False)),
                ('no_of_legs', models.PositiveSmallIntegerField(default=0)),
                ('total_time_in_mins', models.PositiveSmallIntegerField(default=0)),
                ('total_distance_in_kms', models.PositiveSmallIntegerField(default=0)),
                ('legs', models.ManyToManyField(to='polls.FlightLeg')),
            ],
        ),
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('promotion_id', models.AutoField(primary_key=True, serialize=False)),
                ('discount_percent', models.PositiveSmallIntegerField()),
                ('last_valid_date', models.DateTimeField()),
                ('given_cust', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Customer')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('ticket_no', models.AutoField(primary_key=True, serialize=False)),
                ('original_price', models.IntegerField()),
                ('discounted_price', models.IntegerField(null=True)),
                ('promotion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Promotion')),
            ],
        ),
        migrations.RenameField(
            model_name='plane',
            old_name='max_seats',
            new_name='no_of_seats',
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='fligt_leg',
            new_name='flight_leg',
        ),
        migrations.AddField(
            model_name='plane',
            name='seats_per_row',
            field=models.PositiveSmallIntegerField(default=6),
        ),
        migrations.AlterField(
            model_name='crew',
            name='staff_id',
            field=models.OneToOneField(db_column='staff_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='polls.Staff'),
        ),
        migrations.AlterField(
            model_name='hostess',
            name='staff_id',
            field=models.OneToOneField(db_column='staff_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='polls.Staff'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='staff_id',
            field=models.OneToOneField(db_column='staff_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='polls.Staff'),
        ),
        migrations.AlterField(
            model_name='pilot',
            name='license_type',
            field=models.CharField(choices=[('national', 'only in a country'), ('international', 'international flights')], max_length=100),
        ),
        migrations.AlterField(
            model_name='pilot',
            name='staff_id',
            field=models.OneToOneField(db_column='staff_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='polls.Staff'),
        ),
        migrations.AlterField(
            model_name='plane',
            name='model',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='sold_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Salesman'),
        ),
        migrations.AlterField(
            model_name='salesman',
            name='staff_id',
            field=models.OneToOneField(db_column='staff_id', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='polls.Staff'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='manager_id',
            field=models.ForeignKey(blank=True, db_column='manager_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='polls.Manager'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='reservation_code',
            field=models.ForeignKey(db_column='reservation_code', on_delete=django.db.models.deletion.CASCADE, to='polls.Reservation'),
        ),
        migrations.AddField(
            model_name='customer',
            name='flights',
            field=models.ManyToManyField(to='polls.Flight'),
        ),
    ]
