# Generated by Django 3.0.8 on 2020-09-22 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('koj', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='args',
            field=models.CharField(blank=True, default='', max_length=256, verbose_name='명령 인수'),
        ),
    ]