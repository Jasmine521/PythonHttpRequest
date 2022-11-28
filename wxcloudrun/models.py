from datetime import datetime

from django.db import models


# Create your models here.
class Counters(models.Model):
    id = models.AutoField
    count = models.IntegerField(max_length=11, default=0)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Counters'  # 数据库表名
class Record(models.Model):
    id = models.AutoField
    tokenid = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    createtime = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Record'


class Token(models.Model):
    id = models.AutoField
    openid = models.CharField(max_length=100)
    qcshopenid = models.CharField(max_length=100)
    qcshtoken = models.CharField(max_length=100)
    pid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    createtime = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Token'
