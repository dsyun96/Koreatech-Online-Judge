from django.db import models
from koj.models import Problem, Testcase, Submit
from django.conf import settings

# Create your models here.

class Contest(models.Model):
    contest_id = models.AutoField('대회번호', null=False, primary_key=True)
    title = models.CharField(max_length=128)
    winner = models.CharField(max_length=128, null=True, blank=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    def __str__(self):
        return self.title


class ConParticipants(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    participants = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ConProblems(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problems = models.ForeignKey(Problem, on_delete=models.CASCADE)
