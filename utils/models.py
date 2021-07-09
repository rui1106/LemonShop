from django.db import models


class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建数据的时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新数据的时间')

    class Meta:
        abstract = True  # 抽象  告诉django迁移的时候 不创建BaseModel表   只是用来继承的
