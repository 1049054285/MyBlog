# Generated by Django 2.0.3 on 2018-03-25 12:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180325_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleupdown',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='文章'),
        ),
        migrations.AlterField(
            model_name='articleupdown',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者'),
        ),
        migrations.AlterField(
            model_name='commentup',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='评论'),
        ),
        migrations.AlterField(
            model_name='commentup',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='点赞者'),
        ),
        migrations.AlterUniqueTogether(
            name='articleupdown',
            unique_together={('article', 'user', 'is_up')},
        ),
    ]
