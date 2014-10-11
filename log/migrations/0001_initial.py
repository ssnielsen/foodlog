# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.DateField()),
                ('max_cal', models.IntegerField(default=0)),
                ('user_ref', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=255)),
                ('energy', models.DecimalField(max_digits=4, decimal_places=1)),
                ('protein', models.DecimalField(max_digits=4, decimal_places=1)),
                ('carbo', models.DecimalField(max_digits=4, decimal_places=1)),
                ('fat', models.DecimalField(max_digits=4, decimal_places=1)),
                ('public', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Serving',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.IntegerField(default=0)),
                ('meal', models.CharField(max_length=1, choices=[(b'0', b'Breakfast'), (b'1', b'Pre-noon'), (b'2', b'Lunch'), (b'3', b'After-noon'), (b'4', b'Dinner'), (b'5', b'Evening')])),
                ('day', models.ForeignKey(to='log.Day')),
                ('food', models.ForeignKey(to='log.Food')),
            ],
            options={
                'ordering': ['meal'],
            },
            bases=(models.Model,),
        ),
    ]
