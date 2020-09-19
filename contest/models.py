from django.db import models
from koj.models import Problem, Testcase, Submit
from django.conf import settings


# Create your models here.
class Contest(models.Model):
    contest_id = models.AutoField('대회 번호', null=False, primary_key=True)
    title = models.CharField('제목', max_length=128)
    winner = models.CharField('우승자', max_length=128, null=True, blank=True)
    start_time = models.DateTimeField('시작 시간', null=False)
    end_time = models.DateTimeField('종료 시간', null=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '대회'


class ConParticipants(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    participants = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='참가자', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '참가자 선택'


class ConProblems(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problems = models.ForeignKey(Problem, verbose_name='사용할 문제', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '문제 선택'
