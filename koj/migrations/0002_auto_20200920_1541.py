# Generated by Django 3.0.8 on 2020-09-20 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('koj', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='비공개여부'),
        ),
        migrations.AddField(
            model_name='submit',
            name='for_contest',
            field=models.BooleanField(default=False, verbose_name='제출용도'),
        ),
    ]