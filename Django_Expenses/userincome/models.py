from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.

class UserIncome(models.Model):
    amount = models.FloatField(verbose_name="总收入")  # 建议　models.DecimalField
    date = models.DateField(default=now, verbose_name="日期")
    description = models.TextField(verbose_name="描述")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="所属用户")
    source = models.CharField(max_length=256, verbose_name="来源")

    def __str__(self):
        return self.source

    class Meta:
        verbose_name = '收入记录'
        verbose_name_plural = verbose_name
        ordering = ['-date']


class Source(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = '收入来源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
