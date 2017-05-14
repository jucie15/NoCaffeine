# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 07:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pledge', '0006_auto_20170511_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likeordislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_dislike', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='like_dislike',
            field=models.ManyToManyField(through='pledge.LikeOrDislike', to=settings.AUTH_USER_MODEL),
        ),
    ]
