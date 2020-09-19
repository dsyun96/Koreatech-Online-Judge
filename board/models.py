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
    head = models.CharField('분류', max_length=16, choices=HEAD_TYPES)
    title = models.CharField('제목', max_length=126, null=False)
    content = models.TextField('본문')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField('작성 시간', auto_now_add=True)
    views = models.IntegerField('조회수', null=False, default=0)
    recommend = models.IntegerField('추천수', null=False, default=0)
    ip_address = models.GenericIPAddressField('ip 주소')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '게시글'


class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='작성자', on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article, verbose_name='게시글', on_delete=models.CASCADE)
    content = models.TextField('내용')
    created_at = models.DateTimeField('작성 시간', auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = '댓글'
