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
    return 'testcase/{0}/{1}'.format(instance.problem, filename)


class Testcase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.FileField(upload_to=prob_path)
    output_data = models.FileField(upload_to=prob_path)
    is_example = models.BooleanField(default=False)

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
