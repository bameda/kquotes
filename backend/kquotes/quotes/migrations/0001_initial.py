# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-31 18:39
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField(verbose_name='quote')),
                ('external_author', models.TextField(blank=True, verbose_name='external author')),
                ('explanation', models.TextField(blank=True, verbose_name='explanation')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quotes_created', to=settings.AUTH_USER_MODEL, verbose_name='creator')),
            ],
            options={
                'verbose_name_plural': 'quotes',
                'ordering': ['-created_date'],
                'verbose_name': 'quote',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='score')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('quote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scores', to='quotes.Quote', verbose_name='quote')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quote_scores', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name_plural': 'Scores',
                'verbose_name': 'Score',
            },
        ),
        migrations.AddField(
            model_name='quote',
            name='users_rates',
            field=models.ManyToManyField(blank=True, related_name='quotes_rated', through='quotes.Score', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='score',
            unique_together=set([('user', 'quote')]),
        ),
    ]