# Generated by Django 3.0.8 on 2020-09-22 13:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('koj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('contest_id', models.AutoField(primary_key=True, serialize=False, verbose_name='대회 번호')),
                ('title', models.CharField(max_length=128, verbose_name='제목')),
                ('winner', models.CharField(blank=True, max_length=128, null=True, verbose_name='우승자')),
                ('start_time', models.DateTimeField(verbose_name='시작 시간')),
                ('end_time', models.DateTimeField(verbose_name='종료 시간')),
                ('ongoing', models.BooleanField(default=False, verbose_name='진행여부')),
                ('private', models.BooleanField(default=False, verbose_name='비공개 대회 여부')),
                ('participant', models.ManyToManyField(related_name='contest_participants', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '대회',
            },
        ),
        migrations.CreateModel(
            name='ParticipantsSolved',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_solved', models.BooleanField(default=False, verbose_name='정답여부')),
                ('solved_time', models.TimeField(null=True, verbose_name='푼 시간')),
                ('mistakes', models.IntegerField(default=0, verbose_name='오답 횟수')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
                ('participants', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('problems', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='koj.Problem')),
            ],
            options={
                'verbose_name_plural': '참자가가 푼 문제',
            },
        ),
        migrations.CreateModel(
            name='ConProblem',
            fields=[
                ('conp_id', models.AutoField(primary_key=True, serialize=False)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contest.Contest')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='koj.Problem')),
            ],
            options={
                'unique_together': {('contest', 'problem')},
            },
        ),
    ]
