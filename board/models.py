from django.db import models
from django.conf import settings


# Create your models here.
class Article(models.Model):
    HEAD_TYPES = (
        ('N', '자유'),
        ('Q', '질문'),
        ('I', '정보'),
    )

    article_id = models.AutoField('글 번호', null=False, primary_key=True)
    head = models.CharField(max_length=16, choices=HEAD_TYPES)
    title = models.CharField(max_length=126, null=False)
    # content = models.TextField(null=False)
    content = models.TextField()
    #author = models.CharField(max_length=32, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(null=False, default=0)
    rcmd = models.IntegerField(null=False, default=0)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
