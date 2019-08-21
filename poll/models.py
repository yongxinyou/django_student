"""
Django框架内置了ORM(Object-Relational Mapping) 框架
程序中只需要通过操作对象就能够完成数据CRUD(增删改查)操作

python 中的一个对象 对应 数据库的一条记录


Python程序 -- 面向对象模型
MySQL数据库 -- 关系模型
ORM就是可以让面向对象模型和关系模型相互转换
insert - 吧对象模型转换成关系模型
select - 吧关系模型转换成对象模型
"""
from django.db import models


class User(models.Model):
    """用户"""
    no = models.AutoField(primary_key=True, verbose_name='编号')
    username = models.CharField(max_length=20, unique=True, verbose_name='用户名')
    # password用md5摘要，所有用32位
    password = models.CharField(max_length=32, verbose_name='用户密码')
    # 自动设置成当前日期
    regdate = models.DateTimeField(auto_now_add=True, verbose_name='注册日期')
    email = models.CharField(max_length=255, default='', blank=True, verbose_name='邮箱')
    tel = models.CharField(max_length=11, verbose_name='手机号')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Subject(models.Model):
    """学科"""
    no = models.IntegerField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='名称')
    intro = models.CharField(max_length=511, verbose_name='介绍')
    create_date = models.DateField(null=True, verbose_name='成立日期')
    is_hot = models.BooleanField(default=False, verbose_name='是否热门')

    # 把对象变成字符串 - 这里主要是teacher模型管理时，添加学科时，
    # 显示学科的名字
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tb_subject'
        verbose_name = '学科'
        verbose_name_plural = '学科'


class Teacher(models.Model):
    """老师"""
    no = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=15, verbose_name='姓名')
    gender = models.BooleanField(default=True, choices=((True, '男'), (False, '女')), verbose_name='性别')
    birth = models.DateField(null=True, verbose_name='生日')
    tel = models.CharField(max_length=15, null=True, verbose_name='电话')
    intro = models.CharField(max_length=511, default='', verbose_name='介绍')
    good_count = models.IntegerField(default=0, verbose_name='好评')
    bad_count = models.IntegerField(default=0, verbose_name='差评')
    photo = models.CharField(max_length=255, null=True, verbose_name='头像')
    # 在数据库中默认的名字是subject_id
    subject = models.ForeignKey(to=Subject, on_delete=models.PROTECT, db_column='sno', verbose_name='所属学科')

    class Meta:
        db_table = 'tb_teacher'
        verbose_name = '老师'
        verbose_name_plural = '老师'