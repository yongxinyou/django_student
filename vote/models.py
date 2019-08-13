from django.db import models

# Django框架内置了ORM(Object-Relational Mapping) 框架
# 程序中只需要通过操作对象就能够完成数据CRUD(增删改查)操作


class Fruit(models.Model):
    no = models.AutoField(primary_key=True, verbose_name='编号')
    name = models.CharField(max_length=20, verbose_name='名字')
    intro = models.CharField(max_length=511, verbose_name='介绍')
    fav = models.IntegerField(default=0, verbose_name='热度')

    class Meta:
        db_table = 'tb_fruit'
        verbose_name = '水果'
        verbose_name_plural = '水果'