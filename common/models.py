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
    major = models.CharField('학과', max_length=32)
