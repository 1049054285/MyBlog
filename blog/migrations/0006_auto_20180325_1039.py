# Generated by Django 2.0.3 on 2018-03-25 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180324_2133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='create_time',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
    ]
