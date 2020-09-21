from django.db import models

from django.conf import settings
from multiselectfield import MultiSelectField
from koj.models import Problem, Submit

# Create your models here.


class Contest(models.Model):

    LANG = (('0', 'C'),
            ('1', 'C++'),
            ('2', 'Java'),
            ('3', 'Python'))

    contest_id = models.AutoField('대회 번호', null=False, primary_key=True)
    title = models.CharField('제목', max_length=128)
    lang = MultiSelectField(choices=LANG)
    winner = models.CharField('우승자', max_length=128, null=True, blank=True)
    start_time = models.DateTimeField('시작 시간', null=False)
    end_time = models.DateTimeField('종료 시간', null=False)
    ongoing = models.BooleanField('진행여부', default=False)
    private = models.BooleanField('비공개 대회 여부', default=False)
    problem = models.ManyToManyField(Problem, related_name='contest_problems')
    participant = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='contest_participants')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '대회'


class ParticipantsSolved(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    participants = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    problems = models.ForeignKey(Problem, on_delete=models.CASCADE)
    is_solved = models.BooleanField('정답여부', default=False)
    solved_time = models.TimeField('푼 시간')
    mistakes = models.IntegerField('오답 횟수')

    class Meta:
        verbose_name_plural = '참자가가 푼 문제'




