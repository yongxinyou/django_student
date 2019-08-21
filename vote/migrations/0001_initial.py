# Generated by Django 2.1.8 on 2019-08-15 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fruit',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False, verbose_name='编号')),
                ('name', models.CharField(max_length=20, verbose_name='名字')),
                ('intro', models.CharField(max_length=511, verbose_name='介绍')),
                ('fav', models.IntegerField(default=0, verbose_name='热度')),
            ],
            options={
                'verbose_name': '水果',
                'verbose_name_plural': '水果',
                'db_table': 'tb_fruit',
            },
        ),
    ]
