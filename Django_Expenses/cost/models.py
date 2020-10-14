from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.

class Expenses(models.Model):
    amount = models.FloatField(verbose_name="总支出")  # 建议 models.DecimalField
    date = models.DateField(default=now, verbose_name="日期")
    description = models.TextField(verbose_name="描述")
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name="所属用户")
    category = models.CharField(max_length=256, verbose_name="类别")

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = '支出记录'
        verbose_name_plural = verbose_name
        ordering = ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = '支出类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
