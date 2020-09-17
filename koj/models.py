from django.db import models
from django.conf import settings


# Create your models here.
class Problem(models.Model):
    prob_id = models.IntegerField('문제 번호', null=False, unique=True)  # autofield?, (unique=True)
    title = models.CharField('제목', max_length=256)
    body = models.TextField()
    input = models.TextField()
    output = models.TextField()
    time_limit = models.IntegerField(default=1)
    memory_limit = models.IntegerField(default=128)
    made_by = models.CharField(default='admin', max_length=32)

    def __str__(self):
        return str(self.prob_id)


def prob_path(instance, filename):
    return 'upload/{0}/{1}'.format(instance.problem, filename)


class Contest(models.Model):
    contest_id = models.AutoField('대회번호', null=False, primary_key=True)
    title = models.CharField(max_length=128)
    winner = models.CharField(max_length=128, null=True, blank=True)
    start_time = models.DateTimeField(null=False)
    end_time = models.DateTimeField(null=False)

    """
    def save(self, *args, **kwargs):
         if not self.winner:
              self.winner = None
         if not self.problems:
              self.problems = None
         if not self.participant:
              self.participant = None
         super(Contest, self).save(*args, **kwargs)
    """
    def __str__(self):
        return self.title


class ConParticipants(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    participants = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class ConProblems(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    problems = models.ForeignKey(Problem, on_delete=models.CASCADE)


class Testcase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.FileField(upload_to=prob_path)
    output_data = models.FileField(upload_to=prob_path)
    # testinput, output

    def __str__(self):
        return str(self.problem)


class Submit(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lang = models.IntegerField(null=False)
    code = models.TextField(null=False)
    length = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)

    result = models.IntegerField(null=True)
    memory = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)
