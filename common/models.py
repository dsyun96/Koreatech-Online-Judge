from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete_models.CASCADE)

class CustomUser(AbstractUser):
    GENDERS = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
    )

    birth_date = models.DateField(verbose_name='생년월일', null=True)
    gender = models.CharField(verbose_name='성별', max_length=1, choices=GENDERS, null=True)
    rank = models.IntegerField('랭킹', null=True)
    solved = models.IntegerField('푼 문제', null=True)
    submited = models.IntegerField('제출한 문제', null=True)
    major = models.CharField('학과', max_length=32)

#class Ranking(models.Model):
#    username = models.ForeignKey(CustomUserm on_delete=CASCADE)
    #solved = models.IntegerField('푼 문제')
