# Generated by Django 2.1.8 on 2019-08-14 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0002_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='photo',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
