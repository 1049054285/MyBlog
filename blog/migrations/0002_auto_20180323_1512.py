# Generated by Django 2.0.3 on 2018-03-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(default='media/avatar/default.jpg', upload_to='media/avatar/'),
        ),
    ]