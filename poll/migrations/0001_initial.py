# Generated by Django 2.1.8 on 2019-08-14 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('no', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=31)),
                ('intro', models.CharField(max_length=511)),
            ],
            options={
                'db_table': 'tb_subject',
            },
        ),
    ]
