from django.db import models


# Create your models here.

class BookInfo(models.Model):
    title = models.CharField(max_length=20, verbose_name='名称')
    pub_date = models.DateField(verbose_name='发布日期', null=True)
    read = models.IntegerField(default=0, verbose_name='阅读量')
    comment = models.IntegerField(default=0, verbose_name='评论量')
    image = models.ImageField(upload_to='books', verbose_name='图片', null=True)

    class Meta:
        verbose_name = '图书'  # 在admin站点中显示的名称

    def __str__(self):
        """定义每个数据对象的显示信息"""
        return self.title


class HeroInfo(models.Model):
    GENDER_CHOICES = (
        (0, 'male'),
        (1, 'female')
    )
    name = models.CharField(max_length=20, verbose_name='名称')
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, default=0, verbose_name='性别')
    description = models.CharField(max_length=200, null=True, verbose_name='描述信息')
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE, verbose_name='图书')  # 外键
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        verbose_name = '人物信息'

    def __str__(self):
        return self.name
