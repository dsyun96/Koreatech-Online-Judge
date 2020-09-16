from django.db import models
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class Problem(models.Model):
    prob_id = models.IntegerField('문제 번호', null=False, unique=True) #autofield?, (unique=True)
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


class Testcase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input_data = models.FileField(upload_to=prob_path)
    output_data = models.FileField(upload_to=prob_path)
    #testinput, output

    def __str__(self):
        return str(self.problem)


class Submit(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lang = models.IntegerField(null=False)
    code = models.TextField(null=False)
    length = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)

    result = models.CharField(max_length=3, null=True)
    memory = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)

class Article(models.Model):

    HEAD_TYPES = (
            ('N', '자유' ),
            ('Q', '질문' ),
            ('I', '정보'),)

    article_id = models.AutoField('글 번호',null=False, primary_key=True)
    head       = models.CharField(max_length=16, choices=HEAD_TYPES)
    title      = models.CharField(max_length=126, null=False)
    #content    = models.TextField(null=False)
    content    = RichTextUploadingField()
    author     = models.CharField(max_length=32, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    views      = models.IntegerField (null=False, default=0)
    rcmd       = models.IntegerField (null=False, default=0)
    ip_address  = models.GenericIPAddressField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete = models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.content


class Fortest(models.Model):
    ip_adress = models.CharField(max_length=126)
    test = models.TextField()
