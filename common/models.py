from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    MAJORS = (
        ('ME', '기계공학부'),
        ('MSE', '메카트로닉스공학부'),
        ('EE&CE', '전기전자통신공학부'),
        ('CSE', '컴퓨터공학부'),
        ('IDE&AE', '디자인건축공학부'),
        ('EM&CE', '에너지신소재화학공학부'),
        ('IM', '산업경영학부'),
        ('LA', '교양학부'),
        ('HRD', 'HRD학과'),
        ('FT', '융합학과')
    )
    major = models.CharField(verbose_name='학과', max_length=256, choices=MAJORS, null=True)
    freetext = models.TextField(null=True, default='None')

    class Meta:
        verbose_name_plural = '사용자'
